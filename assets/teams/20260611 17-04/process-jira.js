const fs = require('fs');
const path = require('path');

const BASE_DIR = path.resolve(__dirname);
const TOOL_RESULTS_DIR = 'C:/Users/i.klyha/.claude/projects/C--Users-i-klyha-Desktop-Claude-wow-scanner-tool/2e169c3e-fd35-416b-9734-ac338229b7a1/tool-results';

// Map tool result files to projects
const projectFiles = {
  MAW: 'toolu_bdrk_01UR3SjeVcFLab9hMXgR5uDJ.txt',
  AENW: 'toolu_bdrk_011NVCAUQtSHPhV5sBy8nnz3.txt',
  AETVP: 'toolu_bdrk_01SHCJtNjvWDnGA1G5PYSde7.txt',
  PEPI: 'toolu_bdrk_016Bcw3y1dSZeYhKu4mBwpU5.txt',
  RSW: 'toolu_bdrk_018AbNbEUDnERSjpBD8v8w7a.txt',
  EPCW: 'toolu_bdrk_01Y71PN7KGEwfvxHk8UxXnS9.txt',
  PEA: 'toolu_bdrk_01E5XzL81R6tSFJ1SNNn6wbL.txt',
  ASPW: 'toolu_bdrk_01WQ15LRAWRqgGz8HRnkaLRC.txt',
  EEEW: 'toolu_bdrk_01HTtDUctiK89e2X5ix3by2b.txt',
};

// ML project was returned inline (small), handle separately
const mlData = {
  issues: {
    nodes: [
      {
        key: "ML-55",
        fields: {
          summary: "Implement Test DAG MLOps based on SDK",
          issuetype: { name: "Task" },
          created: "2026-05-07T09:52:56.776-0400",
          assignee: { displayName: "Tomasz Teter" },
          priority: { name: "Medium" },
          updated: "2026-05-20T05:25:04.125-0400",
          status: { name: "In Progress" },
          customfield_10114: null
        },
        webUrl: "https://adgear.atlassian.net/browse/ML-55"
      },
      {
        key: "ML-10",
        fields: {
          summary: "Support after MWAA upgrade to 2.10.3",
          issuetype: { name: "Task" },
          created: "2026-04-20T13:55:18.034-0400",
          assignee: { displayName: "Tomasz Teter" },
          priority: { name: "Medium" },
          updated: "2026-04-23T09:43:19.611-0400",
          status: { name: "In Progress" },
          customfield_10114: null
        },
        webUrl: "https://adgear.atlassian.net/browse/ML-10"
      }
    ]
  }
};

// Team definitions
const teams = [
  { name: "PE-WAW-Abyss", file: "pe-waw-abyss-jira", project: "MAW", pattern: "PE - WAW - Abyss", board: "MAW/boards/9980" },
  { name: "Radium", file: "radium-jira", project: "AENW", pattern: "AE - WAW - Radium", board: "AENW/boards/8976" },
  { name: "Europium", file: "europium-jira", project: "AENW", pattern: "AP - WAW - Europium", board: "AENW/boards/8979" },
  { name: "Copernicium", file: "copernicium-jira", project: "AETVP", pattern: "AE - WAW - Copernicium", board: "AETVP/boards/9246" },
  { name: "Mouflons", file: "mouflons-jira", project: "PEPI", pattern: "AS - WAW - Mouflons", board: "PEPI/boards/4503" },
  { name: "Wolves", file: "wolves-jira", project: "PEPI", pattern: "AS - WAW - Wolves", board: "PEPI/boards/4504" },
  { name: "Polonium UF", file: "polonium-uf-jira", project: "RSW", pattern: "AS - WAW - Polonium UF", board: "RSW/boards/10403" },
  { name: "Bigos", file: "bigos-jira", project: "MAW", pattern: "AS - WAW - Bigos", board: "MAW/boards/11439" },
  { name: "Capybaras", file: "capybaras-jira", project: "RSW", pattern: "AS - WAW - Capybaras", board: "RSW/boards/10156" },
  { name: "ML Serving Sturgeons", file: "ml-serving-sturgeons-jira", project: "PEPI", pattern: "T - WAW - ML Sturgeons", board: "PEPI/boards/4090" },
  { name: "ML Platform Pandas", file: "ml-platform-pandas-jira", project: "ML", pattern: "T - WAW - ML Pandas", board: "ML/boards/10470" },
  { name: "EP Core", file: "ep-core-jira", project: "EPCW", pattern: "T - WAW - EP Core", board: "EPCW/boards/10972" },
  { name: "Zurek", file: "zurek-jira", project: "PEA", pattern: "Zurek", board: "PEA/boards/2881" },
  { name: "Igni", file: "igni-jira", project: "ASPW", pattern: "AP - WAW - Igni", board: "ASPW/boards/9477" },
  { name: "SRE", file: "sre-jira", project: "EEEW", pattern: "T - WAW - Embedded SREs SRPOL", board: "EEEW/boards/10332" },
];

const JQL_TEMPLATE = 'project = {PROJECT} AND status IN ("In Progress", "Code Review", "In Development") AND issuetype IN (Story, Bug, Task) AND issuetype != Sub-task';
const EXTRACTED_AT = "2026-06-11T17:04:00+02:00";

// Load all project data
const projectData = {};

for (const [proj, file] of Object.entries(projectFiles)) {
  try {
    const raw = fs.readFileSync(path.join(TOOL_RESULTS_DIR, file), 'utf8');
    const data = JSON.parse(raw);
    projectData[proj] = data.issues.nodes;
    console.log(`Loaded ${proj}: ${data.issues.nodes.length} issues`);
  } catch (err) {
    console.error(`Error loading ${proj}: ${err.message}`);
    projectData[proj] = [];
  }
}

// ML handled separately
projectData['ML'] = mlData.issues.nodes;
console.log(`Loaded ML: ${mlData.issues.nodes.length} issues`);

// Process each team
for (const team of teams) {
  const allIssues = projectData[team.project] || [];

  // Filter by customfield_10114.name
  const filtered = allIssues.filter(issue => {
    const teamField = issue.fields?.customfield_10114;
    return teamField && teamField.name === team.pattern;
  });

  console.log(`\n${team.name} (${team.project}, pattern="${team.pattern}"): ${filtered.length} issues`);

  // Build issue list
  const issues = filtered.map(issue => ({
    key: issue.key,
    type: issue.fields.issuetype.name,
    summary: issue.fields.summary,
    status: issue.fields.status.name,
    assignee: issue.fields.assignee ? issue.fields.assignee.displayName : "Unassigned",
    priority: issue.fields.priority.name,
    created: issue.fields.created,
    updated: issue.fields.updated,
    url: `https://adgear.atlassian.net/browse/${issue.key}`
  }));

  // Build summary
  const byStatus = {};
  const byType = {};
  for (const i of issues) {
    byStatus[i.status] = (byStatus[i.status] || 0) + 1;
    byType[i.type] = (byType[i.type] || 0) + 1;
  }

  const jql = JQL_TEMPLATE.replace('{PROJECT}', team.project);
  const boardUrl = `https://adgear.atlassian.net/jira/software/projects/${team.board}`;

  // JSON output
  const jsonOutput = {
    team: team.name,
    boardUrl: boardUrl,
    projectKey: team.project,
    extractedAt: EXTRACTED_AT,
    teamFieldId: "customfield_10114",
    query: {
      jql: jql,
      queryType: "project_filtered_client_side",
      teamPattern: team.pattern
    },
    summary: {
      total: issues.length,
      byStatus: byStatus,
      byType: byType,
      truncated: false
    },
    issues: issues
  };

  fs.writeFileSync(
    path.join(BASE_DIR, `${team.file}.json`),
    JSON.stringify(jsonOutput, null, 2),
    'utf8'
  );

  // TXT output
  let txt = `Team: ${team.name}\n`;
  txt += `Project: ${team.project}\n`;
  txt += `Board: ${boardUrl}\n`;
  txt += `Extracted: ${EXTRACTED_AT}\n`;
  txt += `Query: project filtered, client-side team matching\n`;
  txt += `Team Pattern: ${team.pattern}\n\n`;
  txt += `=== ACTIVE ISSUES ===\n`;
  txt += `Total: ${issues.length}`;

  const statusParts = [];
  for (const [status, count] of Object.entries(byStatus)) {
    statusParts.push(`${status}: ${count}`);
  }
  if (statusParts.length > 0) {
    txt += ` | ${statusParts.join(' | ')}`;
  }
  txt += `\n\n`;

  for (const i of issues) {
    txt += `[${i.key}] ${i.type}: ${i.summary}\n`;
    txt += `  Assignee: ${i.assignee} | Priority: ${i.priority} | Updated: ${i.updated}\n`;
    txt += `  ${i.url}\n\n`;
  }

  if (issues.length === 0) {
    txt += `No issues found matching team pattern "${team.pattern}" in project ${team.project}.\n`;
  }

  fs.writeFileSync(
    path.join(BASE_DIR, `${team.file}.txt`),
    txt,
    'utf8'
  );
}

console.log('\nDone! All files written.');
