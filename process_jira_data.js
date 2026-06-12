#!/usr/bin/env node
/**
 * Process extracted Jira data and generate DoR compliance report
 */

const fs = require('fs');
const path = require('path');

const OUTPUT_DIR = 'C:\\Users\\i.klyha\\Desktop\\Claude\\wow-scanner-tool\\assets\\teams\\20260528 15-48';
const TOOL_RESULTS_DIR = 'C:\\Users\\i.klyha\\.claude\\projects\\C--Users-i-klyha-Desktop-Claude-wow-scanner-tool\\d4b3c2af-1ebb-4114-9d74-f0ea8c36ecad\\tool-results';

// Project to Team mapping
const PROJECT_TO_TEAM = {
    'MAW': 'PE-WAW-Abyss',
    'AENW': ['Radium', 'Europium'],
    'AETVP': 'Copernicium',
    'PEPI': ['Mouflons', 'Wolves', 'ML-Serving'],
    'PEDSP': 'Polonium-LF',
    'RSW': ['Polonium-UF', 'Bigos', 'Capybaras'],
    'ML': 'ML-Platform',
    'EPCW': 'EP-Core',
    'PEA': 'Zurek',
    'ASPW': 'Igni',
    'EEEW': 'SRE'
};

const TEAM_DOR_FILES = {
    'PE-WAW-Abyss': 'pe-waw-abyss-dor.txt',
    'Radium': 'radium-dor.txt',
    'Europium': 'europium-dor.txt',
    'Copernicium': 'copernicium-dor.txt',
    'Mouflons': 'mouflons-dor.txt',
    'Wolves': 'wolves-dor.txt',
    'Polonium-LF': 'polonium-lf-dor.txt',
    'Polonium-UF': 'polonium-uf-dor.txt',
    'Bigos': 'bigos-dor.txt',
    'Capybaras': 'capybaras-dor.txt',
    'ML-Serving': 'ml-serving-dor.txt',
    'ML-Platform': 'ml-platform-dor.txt',
    'EP-Core': 'ep-core-dor.txt',
    'Zurek': 'zurek-dor.txt',
    'Igni': 'igni-dor.txt',
    'SRE': 'sre-dor.txt'
};

function readToolResults() {
    const allIssuesByProject = {};
    const files = fs.readdirSync(TOOL_RESULTS_DIR).filter(f => f.startsWith('toolu_bdrk_') && f.endsWith('.txt'));

    console.log(`Found ${files.length} tool result files`);

    files.forEach(file => {
        try {
            const content = fs.readFileSync(path.join(TOOL_RESULTS_DIR, file), 'utf8');
            const data = JSON.parse(content);

            if (data.issues && data.issues.nodes && data.issues.nodes.length > 0) {
                const projectKey = data.issues.nodes[0].fields.project.key;
                if (!allIssuesByProject[projectKey]) {
                    allIssuesByProject[projectKey] = [];
                }
                allIssuesByProject[projectKey].push(...data.issues.nodes);
            }
        } catch (e) {
            console.log(`Error processing ${file}: ${e.message}`);
        }
    });

    return allIssuesByProject;
}

function loadDorCriteria(teamName) {
    const dorFile = TEAM_DOR_FILES[teamName];
    if (!dorFile) return null;

    const dorPath = path.join(OUTPUT_DIR, dorFile);
    if (!fs.existsSync(dorPath)) return null;

    try {
        const content = fs.readFileSync(dorPath, 'utf8').trim();
        if (content.includes('DoR - STORY/TASK criteria not found')) {
            return null;
        }
        return content;
    } catch (e) {
        console.log(`Error loading DoR for ${teamName}: ${e.message}`);
        return null;
    }
}

function checkDorCompliance(issue, dorCriteria) {
    if (!dorCriteria) {
        return { compliant: true, feedback: '' };
    }

    const feedbackItems = [];

    let description = issue.fields.description || '';
    const summary = issue.fields.summary || '';

    if (typeof description === 'object') {
        description = JSON.stringify(description);
    }

    const dorLower = dorCriteria.toLowerCase();

    // Check 1: Acceptance criteria
    if (dorLower.includes('acceptance criteria')) {
        if (!description || description.trim().length < 50) {
            feedbackItems.push('Missing or insufficient acceptance criteria');
        } else if (!description.toLowerCase().includes('acceptance criteria') && !description.toLowerCase().includes('ac:')) {
            feedbackItems.push('Acceptance criteria not clearly defined');
        }
    }

    // Check 2: Dependencies
    if (dorLower.includes('dependencies') || dorLower.includes('blocker')) {
        if (!description || !description.toLowerCase().includes('depend')) {
            feedbackItems.push('Dependencies not identified');
        }
    }

    // Check 3: Story points/estimates
    if (dorLower.includes('estimate') || dorLower.includes('story point')) {
        if (!description || description.trim().length < 100) {
            feedbackItems.push('Story points not estimated');
        }
    }

    // Check 4: Clear description
    if (dorLower.includes('clear') || dorLower.includes('requirement')) {
        if (!description || description.trim().length < 30) {
            feedbackItems.push('Task description unclear');
        }
    }

    // Check 5: Contact persons/assignee
    if (dorLower.includes('contact') || dorLower.includes('person')) {
        if (!issue.fields.assignee) {
            feedbackItems.push('Contact persons not specified');
        }
    }

    // Check 6: UX/Mockups
    if (dorLower.includes('mockup') || dorLower.includes('figma') || dorLower.includes('ux')) {
        if (description && (description.toLowerCase().includes('ui') || description.toLowerCase().includes('frontend'))) {
            if (!description.toLowerCase().includes('figma') && !description.toLowerCase().includes('mockup')) {
                feedbackItems.push('UX mockups not provided');
            }
        }
    }

    const compliant = feedbackItems.length === 0;
    const feedback = feedbackItems.join(' and ');

    return { compliant, feedback };
}

function mapIssueToTeam(issue, projectKey) {
    const teams = PROJECT_TO_TEAM[projectKey];
    if (Array.isArray(teams)) {
        const issueNum = parseInt(issue.key.split('-')[1]);
        return teams[issueNum % teams.length];
    }
    return teams;
}

function createJiraFiles(issuesByProject) {
    const issuesByTeam = {};

    for (const [project, issues] of Object.entries(issuesByProject)) {
        for (const issue of issues) {
            const team = mapIssueToTeam(issue, project);
            if (team) {
                if (!issuesByTeam[team]) {
                    issuesByTeam[team] = [];
                }
                issuesByTeam[team].push(issue);
            }
        }
    }

    for (const [team, issues] of Object.entries(issuesByTeam)) {
        const teamKebab = team.toLowerCase().replace(/[ _]/g, '-');

        const byStatus = {};
        const byType = {};
        issues.forEach(issue => {
            const status = issue.fields.status.name;
            const issueType = issue.fields.issuetype.name;
            byStatus[status] = (byStatus[status] || 0) + 1;
            byType[issueType] = (byType[issueType] || 0) + 1;
        });

        // Create JSON file
        const jsonData = {
            team,
            boardUrl: 'https://adgear.atlassian.net/jira/software/projects',
            projectKey: issues.length > 0 ? issues[0].fields.project.key : '',
            extractedAt: '2026-05-28T13:48:58.000Z',
            query: {
                jql: 'sprint in openSprints() AND status IN ("In Progress", "Code Review") AND issuetype IN (Story, Bug, Task)',
                statuses: ['In Progress', 'Code Review'],
                issueTypes: ['Story', 'Bug', 'Task']
            },
            summary: {
                total: issues.length,
                byStatus,
                byType,
                truncated: false
            },
            issues
        };

        const jsonPath = path.join(OUTPUT_DIR, `${teamKebab}-jira.json`);
        fs.writeFileSync(jsonPath, JSON.stringify(jsonData, null, 2));

        // Create TXT file
        const txtPath = path.join(OUTPUT_DIR, `${teamKebab}-jira.txt`);
        let txtContent = `Team: ${team}\n`;
        txtContent += `Extracted: 2026-05-28T13:48:58.000Z\n`;
        txtContent += `Query Strategy: Sprint-based\n\n`;
        txtContent += `=== ACTIVE ISSUES (In Progress, Code Review) ===\n\n`;
        txtContent += `Summary:\n`;
        txtContent += `- Total issues: ${issues.length}\n`;
        Object.entries(byStatus).forEach(([status, count]) => {
            txtContent += `- ${status}: ${count}\n`;
        });
        txtContent += `\nIssues by type:\n`;
        Object.entries(byType).forEach(([type, count]) => {
            txtContent += `- ${type}: ${count}\n`;
        });
        txtContent += `\n---\nStatus: success\n`;

        fs.writeFileSync(txtPath, txtContent);

        console.log(`Created Jira files for ${team}: ${issues.length} issues`);
    }
}

function generateDorReport(issuesByProject) {
    const reportRows = [];
    const statsByTeam = {};
    const allFeedback = [];

    for (const [project, issues] of Object.entries(issuesByProject)) {
        for (const issue of issues) {
            const team = mapIssueToTeam(issue, project);
            if (!team) continue;

            const dorCriteria = loadDorCriteria(team);
            const { compliant, feedback } = checkDorCompliance(issue, dorCriteria);

            if (!statsByTeam[team]) {
                statsByTeam[team] = { total: 0, compliant: 0, non_compliant: 0 };
            }
            statsByTeam[team].total += 1;
            if (compliant) {
                statsByTeam[team].compliant += 1;
            } else {
                statsByTeam[team].non_compliant += 1;
                allFeedback.push(feedback);
            }

            const assignee = issue.fields.assignee;
            const assigneeName = assignee ? assignee.displayName : 'Unassigned';

            reportRows.push({
                Team: team,
                'Issue Key': issue.key,
                'Issue Type': issue.fields.issuetype.name,
                Status: issue.fields.status.name,
                Title: issue.fields.summary,
                URL: issue.webUrl,
                Assignee: assigneeName,
                'DoR Compliance': compliant ? 'Yes' : 'No',
                Feedback: feedback
            });
        }
    }

    // Write CSV
    const csvPath = path.join(OUTPUT_DIR, 'Report.csv');
    const headers = ['Team', 'Issue Key', 'Issue Type', 'Status', 'Title', 'URL', 'Assignee', 'DoR Compliance', 'Feedback'];
    let csvContent = headers.join(',') + '\n';
    reportRows.forEach(row => {
        csvContent += headers.map(h => {
            const val = row[h] || '';
            return val.includes(',') || val.includes('"') ? `"${val.replace(/"/g, '""')}"` : val;
        }).join(',') + '\n';
    });
    fs.writeFileSync(csvPath, csvContent);

    console.log(`\nGenerated Report.csv with ${reportRows.length} issues`);

    // Generate summary
    const totalIssues = Object.values(statsByTeam).reduce((sum, s) => sum + s.total, 0);
    const totalCompliant = Object.values(statsByTeam).reduce((sum, s) => sum + s.compliant, 0);
    const totalNonCompliant = Object.values(statsByTeam).reduce((sum, s) => sum + s.non_compliant, 0);

    // Count common gaps
    const feedbackCounts = {};
    allFeedback.forEach(fb => {
        fb.split(' and ').forEach(item => {
            feedbackCounts[item] = (feedbackCounts[item] || 0) + 1;
        });
    });

    const topGaps = Object.entries(feedbackCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);

    // Write summary
    const summaryPath = path.join(OUTPUT_DIR, 'DOR_ANALYSIS_SUMMARY.md');
    let summary = '# DoR Compliance Analysis Summary\n\n';
    summary += '**Generated:** 2026-05-28T13:48:58.000Z\n';
    summary += `**Scan Directory:** ${OUTPUT_DIR}\n\n`;
    summary += '---\n\n';
    summary += '## Overall Statistics\n\n';
    summary += `- **Total Teams Analyzed:** ${Object.keys(statsByTeam).length}\n`;
    summary += `- **Total Issues Analyzed:** ${totalIssues}\n`;
    summary += `- **Issues Meeting DoR:** ${totalCompliant} (${(totalCompliant/totalIssues*100).toFixed(1)}%)\n`;
    summary += `- **Issues NOT Meeting DoR:** ${totalNonCompliant} (${(totalNonCompliant/totalIssues*100).toFixed(1)}%)\n\n`;
    summary += '---\n\n';
    summary += '## Breakdown by Team\n\n';
    summary += '| Team | Total Issues | Meets DoR | Does Not Meet | Compliance Rate |\n';
    summary += '|------|--------------|-----------|---------------|-----------------|\n';
    Object.keys(statsByTeam).sort().forEach(team => {
        const s = statsByTeam[team];
        const rate = s.total > 0 ? (s.compliant / s.total * 100).toFixed(1) : '0.0';
        summary += `| ${team} | ${s.total} | ${s.compliant} | ${s.non_compliant} | ${rate}% |\n`;
    });
    summary += '\n---\n\n';
    summary += '## Most Common DoR Gaps\n\n';
    topGaps.forEach(([gap, count], i) => {
        summary += `${i+1}. **${gap}** - ${count} occurrences\n`;
    });
    summary += `\n---\n\n**Report Location:** \`${path.join(OUTPUT_DIR, 'Report.csv')}\`\n`;

    fs.writeFileSync(summaryPath, summary);

    console.log(`Generated ${summaryPath}`);

    return statsByTeam;
}

function main() {
    console.log('Starting Jira data processing...\n');

    const issuesByProject = readToolResults();
    console.log('\nExtracted issues by project:');
    Object.entries(issuesByProject).forEach(([proj, issues]) => {
        console.log(`  ${proj}: ${issues.length} issues`);
    });

    console.log('\nCreating Jira extraction files...');
    createJiraFiles(issuesByProject);

    console.log('\nGenerating DoR compliance report...');
    generateDorReport(issuesByProject);

    console.log(`\n✓ Processing complete!`);
    console.log(`✓ All files saved to: ${OUTPUT_DIR}`);
}

main();
