<%*
const match = tp.file.title.match(/(\d{4}-\d{2}-\d{2})/);
// Calendar plugins may create "Untitled" first and rename afterwards.
// If the title has no date yet, fall back to today so the script still completes.
const today = match ? moment(match[1], 'YYYY-MM-DD') : moment();
const yesterday = today.clone().subtract(1, 'day').format('YYYY-MM-DD');
const tomorrow = today.clone().add(1, 'day').format('YYYY-MM-DD');
const oneYearAgo = today.clone().subtract(1, 'year').format('YYYY-MM-DD');
const dateStr = today.format('YYYY-MM-DD');
const monday = today.clone().startOf('isoWeek');
const weekNote = monday.format('GGGG-WW') + 'W';
const monthNote = today.format('YYYY-MM');

// After the daily note is saved, create the surrounding dashboards sequentially.
const dashboardFolderPath = '10. Time/06 Dashboard';
const dashboardTemplatePath = '90. Settings/02 Templates/auto/Dashboard.template.md';
const createDashboard = tp.file.create_new;
tp.hooks.on_all_templates_executed(async () => {
	const dashboardFolder = tp.app.vault.getAbstractFileByPath(dashboardFolderPath);
	const dashboardTemplate = tp.app.vault.getAbstractFileByPath(dashboardTemplatePath);
	if (!(dashboardFolder instanceof tp.obsidian.TFolder) ||
		!(dashboardTemplate instanceof tp.obsidian.TFile)) {
		new tp.obsidian.Notice('Dashboard creation requires its folder and template. Check the Daily Note template paths.');
		return;
	}
	for (const date of [yesterday, dateStr, tomorrow]) {
		const path = `${dashboardFolderPath}/${date} Dashboard.md`;
		if (tp.app.vault.getAbstractFileByPath(path)) continue;
		try {
			const dashboard = await createDashboard(
				dashboardTemplate, `${date} Dashboard`, false, dashboardFolder);
			if (!dashboard) throw new Error('Templater returned no dashboard file');
		} catch (e) {
			console.error('[Dashboard] create failed: ' + date, e);
			new tp.obsidian.Notice(`Dashboard creation failed for ${date}. Check the developer console.`);
		}
	}
});
-%>
---
up: "[[<% dateStr %> Dashboard]]"
week: "[[<% weekNote %>]]"
month: "[[<% monthNote %>]]"
type: log
created_by: user
authorship: user
tags:
  - daily
---
[[<% yesterday %>|Yesterday (<% yesterday %>)]] | [[<% oneYearAgo %>|1 Year Ago]] | [[<% tomorrow %>|Tomorrow (<% tomorrow %>)]]

## Thinking

## To do

## Reflection

## Thanks
