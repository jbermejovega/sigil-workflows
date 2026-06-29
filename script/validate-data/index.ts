#!/usr/bin/env npx ts-node
import { promises as fs } from "fs";
import { safeLoad } from "js-yaml";
import { basename, extname, join, dirname } from "path";
import { Validator as validator } from "jsonschema";
import { endGroup, error, info, setFailed, startGroup } from '@actions/core';

interface WorkflowWithErrors {
  id: string;
  name: string;
  errors: string[];
}

interface WorkflowProperties {
  name: string;
  description: string;
  creator: string;
  iconName: string;
  categories: string[];
}

interface WorkflowStep {
  name?: string;
  uses?: string;
  run?: string;
}

interface WorkflowJob {
  steps?: WorkflowStep[];
}

interface WorkflowTemplate {
  name?: string;
  permissions?: { [key: string]: string };
  jobs?: { [key: string]: WorkflowJob };
}

interface RequiredPermission {
  key: string;
  value: string;
}

interface WorkflowInvariant {
  id: string;
  workflowPath: string;
  expectedWorkflowName: string;
  expectedTemplateName: string;
  requiredCategories: string[];
  requiredPermission: RequiredPermission;
  requiredUses: string[];
  requiredStepNames: string[];
  requiredRunFragments: string[];
  forbiddenRunFragments: string[];
}

const workflowInvariants: WorkflowInvariant[] = [
  {
    id: "compu2526-review",
    workflowPath: "../../ci/compu2526-review.yml",
    expectedWorkflowName: "COMPU2526 review",
    expectedTemplateName: "COMPU2526 assignment review",
    requiredCategories: [
      "Continuous integration",
      "Python",
      "C",
      "C++",
      "Jupyter Notebook",
      "Education"
    ],
    requiredPermission: {
      key: "contents",
      value: "read"
    },
    requiredUses: [
      "actions/checkout@v4",
      "actions/setup-python@v5"
    ],
    requiredStepNames: [
      "Checkout",
      "Set up Python",
      "Report repository manifests",
      "Check Python syntax",
      "Check C syntax",
      "Check C++ syntax",
      "Check notebooks",
      "Print manual review gates"
    ],
    requiredRunFragments: [
      "python -m py_compile",
      "gcc -std=c11 -fsyntax-only",
      "g++ -std=c++17 -fsyntax-only",
      "json.load(handle)",
      "Large notebook",
      "Manual review still required",
      "parameters and random seeds logged",
      "units and rescaling documented",
      "conserved quantities checked",
      "generated data and media provenance clear"
    ],
    forbiddenRunFragments: [
      "pytest",
      "make check",
      "make distcheck",
      "jupyter nbconvert --execute"
    ]
  }
];

const propertiesSchema = {
  type: "object",
  properties: {
    name: { type: "string", required: true , "minLength": 1},
    description: { type: "string", required: true },
    creator: { type: "string", required: false },
    iconName: { type: "string", required: true },
    categories: {
      anyOf: [
        {
          type: "array",
          items: { type: "string" }
        },
        {
          type: "null",
        }
      ],
      required: true
    },
  }
}

function normalizedPath(path: string): string {
  return path.replace(/\\/g, "/");
}

function allSteps(workflow: WorkflowTemplate): WorkflowStep[] {
  if (!workflow.jobs) {
    return [];
  }

  const steps: WorkflowStep[] = [];
  Object.keys(workflow.jobs).forEach(jobName => {
    const job = workflow.jobs[jobName];
    if (job && Array.isArray(job.steps)) {
      job.steps.forEach(step => steps.push(step));
    }
  });
  return steps;
}

function runText(steps: WorkflowStep[]): string {
  return steps
    .map(step => step.run || "")
    .join("\n");
}

function usesValues(steps: WorkflowStep[]): string[] {
  return steps
    .map(step => step.uses)
    .filter(uses => !!uses) as string[];
}

function checkWorkflowInvariants(
  workflowPath: string,
  workflow: WorkflowTemplate,
  properties: WorkflowProperties
): string[] {
  const invariant = workflowInvariants.find(candidate =>
    normalizedPath(workflowPath) == normalizedPath(candidate.workflowPath)
  );
  if (!invariant) {
    return [];
  }

  const errors: string[] = [];
  const steps = allSteps(workflow);
  const names = steps.map(step => step.name || "");
  const runs = runText(steps);
  const uses = usesValues(steps);

  if (workflow.name != invariant.expectedWorkflowName) {
    errors.push(`Invariant ${invariant.id}: workflow name must be "${invariant.expectedWorkflowName}"`);
  }

  if (properties.name != invariant.expectedTemplateName) {
    errors.push(`Invariant ${invariant.id}: properties name must be "${invariant.expectedTemplateName}"`);
  }

  const permissionValue = workflow.permissions && workflow.permissions[invariant.requiredPermission.key];
  if (permissionValue != invariant.requiredPermission.value) {
    errors.push(
      `Invariant ${invariant.id}: permission ${invariant.requiredPermission.key} must be ${invariant.requiredPermission.value}`
    );
  }

  invariant.requiredCategories.forEach(category => {
    if (!properties.categories || properties.categories.indexOf(category) == -1) {
      errors.push(`Invariant ${invariant.id}: missing category "${category}"`);
    }
  });

  invariant.requiredUses.forEach(requiredUse => {
    if (uses.indexOf(requiredUse) == -1) {
      errors.push(`Invariant ${invariant.id}: missing action use "${requiredUse}"`);
    }
  });

  invariant.requiredStepNames.forEach(stepName => {
    if (names.indexOf(stepName) == -1) {
      errors.push(`Invariant ${invariant.id}: missing step "${stepName}"`);
    }
  });

  invariant.requiredRunFragments.forEach(fragment => {
    if (runs.indexOf(fragment) == -1) {
      errors.push(`Invariant ${invariant.id}: missing run fragment "${fragment}"`);
    }
  });

  invariant.forbiddenRunFragments.forEach(fragment => {
    if (runs.indexOf(fragment) != -1) {
      errors.push(`Invariant ${invariant.id}: forbidden run fragment "${fragment}"`);
    }
  });

  return errors;
}

async function checkWorkflows(folders: string[], allowed_categories: object[]): Promise<WorkflowWithErrors[]> {
  const result: WorkflowWithErrors[] = []
  const workflow_template_names = new Set()
  for (const folder of folders) {
    const dir = await fs.readdir(folder, {
      withFileTypes: true,
    });

    for (const e of dir) {
      if (e.isFile() && [".yml", ".yaml"].includes(extname(e.name))) {
        const fileType = basename(e.name, extname(e.name))

        const workflowFilePath = join(folder, e.name);
        const propertiesFilePath = join(folder, "properties", `${fileType}.properties.json`)

        const workflowWithErrors = await checkWorkflow(workflowFilePath, propertiesFilePath, allowed_categories);
        if(workflowWithErrors.name && workflow_template_names.size == workflow_template_names.add(workflowWithErrors.name).size) {
          workflowWithErrors.errors.push(`Workflow template name "${workflowWithErrors.name}" already exists`) 
        }
        if (workflowWithErrors.errors.length > 0) {
          result.push(workflowWithErrors)
        }
      }
    }
  }

  return result;
}

async function checkWorkflow(workflowPath: string, propertiesPath: string, allowed_categories: object[]): Promise<WorkflowWithErrors> {
  let workflowErrors: WorkflowWithErrors = {
    id: workflowPath,
    name: null,
    errors: []
  }
  try {
    const workflowFileContent = await fs.readFile(workflowPath, "utf8");
    const workflow = safeLoad(workflowFileContent) as WorkflowTemplate; // Validate yaml parses without error

    const propertiesFileContent = await fs.readFile(propertiesPath, "utf8")
    const properties: WorkflowProperties = JSON.parse(propertiesFileContent)
    if(properties.name && properties.name.trim().length > 0) {
      workflowErrors.name = properties.name
    }
    let v = new validator();
    const res = v.validate(properties, propertiesSchema)
    workflowErrors.errors = res.errors.map(e => e.toString())
    
    if (properties.iconName) {
      if(! /^octicon\s+/.test(properties.iconName)) {
        try {
          await fs.access(`../../icons/${properties.iconName}.svg`)
        } catch (e) {
          workflowErrors.errors.push(`No icon named ${properties.iconName} found`)
        }
      }
      else {
        let iconName = properties.iconName.match(/^octicon\s+(.*)/)
        if(!iconName || iconName[1].split(".")[0].length <= 0) {
          workflowErrors.errors.push(`No icon named ${properties.iconName} found`)
        }
      }
      
    }
    var path = dirname(workflowPath)
    var folder_categories = allowed_categories.find( category => category["path"] == path)["categories"]
    if (!workflowPath.endsWith("blank.yml")) {
      if(!properties.categories || properties.categories.length == 0) {
        workflowErrors.errors.push(`Workflow categories cannot be null or empty`)
      } 
      else if(!folder_categories.some(category => properties.categories[0].toLowerCase() == category.toLowerCase())) {
        workflowErrors.errors.push(`The first category in properties.json categories for workflow in ${basename(path)} folder must be one of "${folder_categories}. Either move the workflow to an appropriate directory or change the category."`)
      }
    }

    if(basename(path).toLowerCase() == 'deployments' && !properties.creator) {
      workflowErrors.errors.push(`The "creator" in properties.json must be present.`)
    }

    workflowErrors.errors = workflowErrors.errors.concat(
      checkWorkflowInvariants(workflowPath, workflow, properties)
    )
  } catch (e) {
    workflowErrors.errors.push(e.toString())
  }
  return workflowErrors;
}

(async function main() {
  try {
    const settings = require("./settings.json");
    const erroredWorkflows = await checkWorkflows(
      settings.folders, settings.allowed_categories
    )

    if (erroredWorkflows.length > 0) {
      startGroup(`Found ${erroredWorkflows.length} workflows with errors:`);
      erroredWorkflows.forEach(erroredWorkflow => {
        error(`Errors in ${erroredWorkflow.id} - ${erroredWorkflow.errors.map(e => e.toString()).join(", ")}`)
      })
      endGroup();
      setFailed(`Found ${erroredWorkflows.length} workflows with errors`);
    } else {
      info("Found no workflows with errors!")
    }
  } catch (e) {
    error(`Unhandled error while syncing workflows: ${e}`);
    setFailed(`Unhandled error`)
  }
})();
