// Parse SRPOL Teams table and extract team information
const fs = require('fs');
const path = require('path');

// HTML content from Confluence
const htmlContent = `<table data-width="1800"><thead><tr><th><p><strong>SRPOL Ads Team</strong></p></th><th><p><strong>Team Type</strong></p></th><th><p><strong>Product/Responsibility</strong></p></th><th><p><strong>Product Domain / Area</strong></p></th><th><p><strong>SPRINT board</strong></p></th><th><p><strong>Group Lead (GL)</strong><br>Part Lead (PL)</p></th><th><p><strong>PO / SM / Tech Lead</strong></p></th><th><p><strong>Product Managers</strong></p></th><th><p><strong>Architect</strong></p></th><th><p><strong>Dashboards</strong></p></th></tr></thead><tbody>`;

// Extract page ID from Confluence URL
function extractPageId(url) {
  if (!url) return null;

  // Handle tiny link format: /wiki/x/WID6RQU
  const tinyMatch = url.match(/\/wiki\/x\/([A-Za-z0-9_-]+)/);
  if (tinyMatch) {
    return tinyMatch[1]; // Return the tiny link ID
  }

  // Handle full page format: /wiki/spaces/ENG/pages/21730492571
  const pageMatch = url.match(/\/pages\/(\d+)/);
  if (pageMatch) {
    return pageMatch[1];
  }

  return null;
}

// Extract team name from URL or content
function extractTeamName(htmlRow) {
  // Try to extract from link text or page title
  const linkMatch = htmlRow.match(/<a[^>]*>([^<]+)<\/a>/);
  if (linkMatch) {
    const text = linkMatch[1].trim();
    // Remove common suffixes
    return text
      .replace(/\s*-\s*Engineering\s*-\s*Confluence/gi, '')
      .replace(/SRPOL Ads\s*<TEAM>\s*template/gi, 'Template')
      .replace(/https:\/\/[^\s]+/g, '')
      .trim();
  }
  return 'Unknown';
}

// Clean text content
function cleanText(html) {
  if (!html) return '';
  return html
    .replace(/<[^>]+>/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/\s+/g, ' ')
    .trim();
}

// Parse table rows
function parseTeamTable(html) {
  const teams = [];
  const rows = html.split(/<tr[^>]*>/);

  for (let i = 1; i < rows.length; i++) {
    const row = rows[i];
    if (!row.includes('</tr>')) continue;

    const cells = row.match(/<td[^>]*>.*?<\/td>/gs);
    if (!cells || cells.length < 5) continue;

    // Skip template row
    if (row.includes('SRPOL Ads <TEAM> template')) continue;

    // Extract data
    const teamPageCell = cells[0] || '';
    const teamTypeCell = cells[1] || '';
    const productCell = cells[2] || '';
    const domainCell = cells[3] || '';
    const sprintBoardCell = cells[4] || '';

    // Extract URLs
    const teamPageMatch = teamPageCell.match(/href="([^"]+)"/);
    const teamPageUrl = teamPageMatch ? teamPageMatch[1] : null;
    const sprintBoardMatch = sprintBoardCell.match(/href="([^"]+)"/);
    const sprintBoardUrl = sprintBoardMatch ? sprintBoardMatch[1] : null;

    if (!teamPageUrl || teamPageUrl.includes('TEAM')) continue;

    const pageId = extractPageId(teamPageUrl);
    const teamName = extractTeamName(teamPageCell);

    teams.push({
      name: teamName,
      team_page_url: teamPageUrl,
      team_page_id: pageId,
      sprint_board_url: sprintBoardUrl,
      team_type: cleanText(teamTypeCell),
      product: cleanText(productCell),
      domain: cleanText(domainCell),
      dor_status: 'pending'
    });
  }

  return teams;
}

// This will be populated with the actual HTML
const teams = parseTeamTable(htmlContent);

console.log(JSON.stringify(teams, null, 2));
