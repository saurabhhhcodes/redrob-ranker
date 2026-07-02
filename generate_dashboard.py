#!/usr/bin/env python3
import json
import csv

def main():
    print("Loading top 100 candidate IDs from team_saurabh.csv...")
    top_candidates = []
    with open("team_saurabh.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            top_candidates.append({
                "candidate_id": row["candidate_id"],
                "rank": int(row["rank"]),
                "score": float(row["score"]),
                "reasoning": row["reasoning"]
            })
            
    top_ids = {c["candidate_id"]: c for c in top_candidates}
    
    print("Extracting full candidate details from candidates.jsonl...")
    candidate_details = {}
    with open("candidates.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                cand = json.loads(line)
                cid = cand["candidate_id"]
                if cid in top_ids:
                    # Merge rank, score, and reasoning
                    cand["rank"] = top_ids[cid]["rank"]
                    cand["score"] = top_ids[cid]["score"]
                    cand["reasoning"] = top_ids[cid]["reasoning"]
                    candidate_details[cid] = cand
                    
    # Sort candidate details by rank
    sorted_details = [candidate_details[c["candidate_id"]] for c in top_candidates if c["candidate_id"] in candidate_details]
    
    # Generate HTML content
    print("Generating self-contained dashboard.html...")
    
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redrob Candidate Discovery Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #0B0F19;
            --bg-card: rgba(20, 27, 45, 0.7);
            --bg-sidebar: #111827;
            --accent-primary: #7C3AED;
            --accent-secondary: #10B981;
            --accent-glow: rgba(124, 58, 237, 0.15);
            --text-primary: #F3F4F6;
            --text-secondary: #9CA3AF;
            --border-color: rgba(255, 255, 255, 0.08);
            --font-main: 'Plus Jakarta Sans', sans-serif;
            --font-title: 'Outfit', sans-serif;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: var(--font-main);
            background-color: var(--bg-main);
            color: var(--text-primary);
            height: 100vh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        /* Header Styling */
        header {
            background-color: var(--bg-sidebar);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            z-index: 10;
        }

        .header-title-container h1 {
            font-family: var(--font-title);
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #A78BFA, #34D399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header-stats {
            display: flex;
            gap: 1.5rem;
        }

        .stat-badge {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-color);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .stat-badge strong {
            color: var(--accent-secondary);
        }

        /* Layout */
        .dashboard-container {
            display: flex;
            flex: 1;
            overflow: hidden;
        }

        /* Sidebar - Candidate List */
        .sidebar {
            width: 380px;
            background-color: var(--bg-sidebar);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .search-container {
            padding: 1.2rem;
            border-bottom: 1px solid var(--border-color);
        }

        .search-input {
            width: 100%;
            padding: 0.8rem 1rem;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            background: rgba(255, 255, 255, 0.02);
            color: var(--text-primary);
            font-family: var(--font-main);
            outline: none;
            transition: all 0.3s;
        }

        .search-input:focus {
            border-color: var(--accent-primary);
            box-shadow: 0 0 10px var(--accent-glow);
        }

        .candidate-list {
            flex: 1;
            overflow-y: auto;
            padding: 0.5rem 0;
        }

        .candidate-item {
            padding: 1rem 1.2rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.02);
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .candidate-item:hover {
            background: rgba(255, 255, 255, 0.02);
        }

        .candidate-item.active {
            background: rgba(124, 58, 237, 0.08);
            border-left: 4px solid var(--accent-primary);
        }

        .rank-circle {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, var(--accent-primary), #6366F1);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.9rem;
            color: white;
            flex-shrink: 0;
        }

        .candidate-meta {
            flex: 1;
            min-width: 0;
        }

        .candidate-meta h3 {
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 0.2rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .candidate-meta p {
            font-size: 0.8rem;
            color: var(--text-secondary);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .score-pill {
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.2);
            color: var(--accent-secondary);
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        /* Detail View */
        .main-content {
            flex: 1;
            padding: 2rem;
            overflow-y: auto;
            background: linear-gradient(180deg, #0B0F19 0%, #080B12 100%);
        }

        .detail-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 2rem;
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        .profile-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 1.5rem;
            margin-bottom: 1.5rem;
        }

        .profile-title h2 {
            font-family: var(--font-title);
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }

        .profile-title h4 {
            color: var(--accent-primary);
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 0.4rem;
        }

        .profile-title p {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .profile-reasoning {
            background: rgba(124, 58, 237, 0.05);
            border: 1px solid rgba(124, 58, 237, 0.15);
            padding: 1.2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            position: relative;
        }

        .profile-reasoning h5 {
            color: #A78BFA;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.4rem;
        }

        .profile-reasoning p {
            font-size: 0.95rem;
            line-height: 1.5;
            color: var(--text-primary);
        }

        .section-title {
            font-family: var(--font-title);
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            border-left: 3px solid var(--accent-primary);
            padding-left: 0.6rem;
        }

        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        /* Career & Edu */
        .timeline-item {
            position: relative;
            padding-left: 1.5rem;
            border-left: 2px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 1.5rem;
        }

        .timeline-item:last-child {
            padding-bottom: 0;
        }

        .timeline-dot {
            position: absolute;
            left: -5px;
            top: 4px;
            width: 8px;
            height: 8px;
            background: var(--accent-primary);
            border-radius: 50%;
        }

        .timeline-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.3rem;
        }

        .timeline-header h4 {
            font-size: 0.95rem;
            font-weight: 600;
        }

        .timeline-header span {
            font-size: 0.8rem;
            color: var(--text-secondary);
        }

        .timeline-sub {
            font-size: 0.85rem;
            color: var(--accent-secondary);
            margin-bottom: 0.5rem;
        }

        .timeline-desc {
            font-size: 0.85rem;
            color: var(--text-secondary);
            line-height: 1.4;
        }

        /* Skills list */
        .skills-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 2rem;
        }

        .skill-tag {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-color);
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            font-size: 0.8rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .skill-tag.expert {
            border-color: rgba(16, 185, 129, 0.3);
            background: rgba(16, 185, 129, 0.05);
        }

        .skill-tag.advanced {
            border-color: rgba(99, 102, 241, 0.3);
            background: rgba(99, 102, 241, 0.05);
        }

        .skill-badge {
            font-size: 0.7rem;
            text-transform: uppercase;
            padding: 0.1rem 0.3rem;
            border-radius: 4px;
            font-weight: 600;
        }

        .skill-badge.expert { color: var(--accent-secondary); background: rgba(16, 185, 129, 0.1); }
        .skill-badge.advanced { color: #818CF8; background: rgba(99, 102, 241, 0.1); }
        .skill-badge.intermediate { color: #FBBF24; background: rgba(251, 191, 36, 0.1); }
        .skill-badge.beginner { color: var(--text-secondary); background: rgba(255, 255, 255, 0.05); }

        /* Signals */
        .signals-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
        }

        .signal-card {
            background: rgba(255, 255, 255, 0.01);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
        }

        .signal-card h6 {
            color: var(--text-secondary);
            font-size: 0.75rem;
            text-transform: uppercase;
            margin-bottom: 0.3rem;
        }

        .signal-card p {
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        .signal-card p.success {
            color: var(--accent-secondary);
        }

        .signal-card p.warning {
            color: #FBBF24;
        }
    </style>
</head>
<body>
    <header>
        <div class="header-title-container">
            <h1>Redrob Candidate Discovery</h1>
        </div>
        <div class="header-stats">
            <div class="stat-badge">Total Scanned: <strong>100,000</strong></div>
            <div class="stat-badge">Top Matches: <strong>100</strong></div>
            <div class="stat-badge">Honeypots Discarded: <strong style="color: #EF4444;">81</strong></div>
        </div>
    </header>

    <div class="dashboard-container">
        <!-- Sidebar Candidate List -->
        <div class="sidebar">
            <div class="search-container">
                <input type="text" class="search-input" id="search" placeholder="Search by name, title, or skills..." oninput="filterCandidates()">
            </div>
            <div class="candidate-list" id="candidatesList">
                <!-- Javascript will populate this -->
            </div>
        </div>

        <!-- Detail Main Panel -->
        <div class="main-content">
            <div class="detail-card" id="detailCard">
                <!-- Javascript will populate this on selection -->
                <div style="text-align: center; padding: 5rem 0; color: var(--text-secondary);">
                    Select a candidate from the sidebar to inspect details
                </div>
            </div>
        </div>
    </div>

    <script>
        const candidates = JSON.parse(decodeURIComponent('CANDIDATE_DATA_PLACEHOLDER'));

        function populateList(list) {
            const listEl = document.getElementById('candidatesList');
            listEl.innerHTML = '';
            list.forEach((c) => {
                const item = document.createElement('div');
                item.className = 'candidate-item';
                item.onclick = () => selectCandidate(c.candidate_id);
                item.id = `cand-${c.candidate_id}`;

                item.innerHTML = `
                    <div class="rank-circle">${c.rank}</div>
                    <div class="candidate-meta">
                        <h3>${c.profile.anonymized_name}</h3>
                        <p>${c.profile.current_title} • ${c.profile.years_of_experience} yrs exp</p>
                    </div>
                    <div class="score-pill">${c.score.toFixed(1)}</div>
                `;
                listEl.appendChild(item);
            });
        }

        function filterCandidates() {
            const query = document.getElementById('search').value.toLowerCase();
            const filtered = candidates.filter(c => {
                const name = c.profile.anonymized_name.toLowerCase();
                const title = c.profile.current_title.toLowerCase();
                const summary = c.profile.summary.toLowerCase();
                const skills = c.skills.map(s => s.name.toLowerCase()).join(' ');
                return name.includes(query) || title.includes(query) || summary.includes(query) || skills.includes(query);
            });
            populateList(filtered);
            if(filtered.length > 0) {
                selectCandidate(filtered[0].candidate_id);
            }
        }

        function selectCandidate(id) {
            // Remove active classes
            document.querySelectorAll('.candidate-item').forEach(el => el.classList.remove('active'));
            const activeEl = document.getElementById(`cand-${id}`);
            if (activeEl) activeEl.classList.add('active');

            const cand = candidates.find(c => c.candidate_id === id);
            if (!cand) return;

            const detailEl = document.getElementById('detailCard');
            
            // Build career timeline
            const careerHtml = cand.career_history.map(job => `
                <div class="timeline-item">
                    <div class="timeline-dot"></div>
                    <div class="timeline-header">
                        <h4>${job.title}</h4>
                        <span>${job.start_date} - ${job.end_date || 'Present'} (${job.duration_months} mo)</span>
                    </div>
                    <div class="timeline-sub">${job.company} • ${job.company_size} • ${job.industry}</div>
                    <p class="timeline-desc">${job.description}</p>
                </div>
            `).join('');

            // Build education timeline
            const eduHtml = cand.education.map(edu => `
                <div class="timeline-item">
                    <div class="timeline-dot" style="background: var(--accent-secondary);"></div>
                    <div class="timeline-header">
                        <h4>${edu.degree} in ${edu.field_of_study}</h4>
                        <span>${edu.start_year} - ${edu.end_year}</span>
                    </div>
                    <div class="timeline-sub">${edu.institution} • ${edu.tier}</div>
                </div>
            `).join('');

            // Build skills tags
            const skillsHtml = cand.skills.map(s => `
                <div class="skill-tag ${s.proficiency}">
                    <span>${s.name}</span>
                    <span class="skill-badge ${s.proficiency}">${s.proficiency}</span>
                </div>
            `).join('');

            // Format notice period
            let noticeClass = 'success';
            if (cand.redrob_signals.notice_period_days > 90) noticeClass = 'warning';

            detailEl.innerHTML = `
                <div class="profile-header">
                    <div class="profile-title">
                        <h2>${cand.profile.anonymized_name}</h2>
                        <h4>${cand.profile.current_title}</h4>
                        <p>${cand.profile.location}, ${cand.profile.country} • ${cand.profile.years_of_experience} Years Stated Experience</p>
                    </div>
                    <div style="text-align: right;">
                        <div class="rank-circle" style="width: 50px; height: 50px; font-size: 1.3rem; margin-bottom: 0.5rem; margin-left: auto;">${cand.rank}</div>
                        <div class="score-pill" style="font-size: 0.9rem; padding: 0.3rem 0.8rem;">Score: ${cand.score.toFixed(1)}</div>
                    </div>
                </div>

                <div class="profile-reasoning">
                    <h5>Redrob AI Match Reasoning</h5>
                    <p>${cand.reasoning}</p>
                </div>

                <div class="grid-2">
                    <div>
                        <h3 class="section-title">Career History</h3>
                        <div>${careerHtml}</div>
                    </div>
                    <div>
                        <h3 class="section-title">Education</h3>
                        <div style="margin-bottom: 1.5rem;">${eduHtml}</div>

                        <h3 class="section-title">Platform Engagement Signals</h3>
                        <div class="signals-grid">
                            <div class="signal-card">
                                <h6>Response Rate</h6>
                                <p class="success">${(cand.redrob_signals.recruiter_response_rate * 100).toFixed(0)}%</p>
                            </div>
                            <div class="signal-card">
                                <h6>Notice Period</h6>
                                <p class="${noticeClass}">${cand.redrob_signals.notice_period_days} Days</p>
                            </div>
                            <div class="signal-card">
                                <h6>GitHub Score</h6>
                                <p>${cand.redrob_signals.github_activity_score >= 0 ? cand.redrob_signals.github_activity_score.toFixed(0) : 'N/A'}</p>
                            </div>
                            <div class="signal-card">
                                <h6>Salary Min/Max</h6>
                                <p style="font-size: 0.85rem;">${cand.redrob_signals.expected_salary_range_inr_lpa.min} - ${cand.redrob_signals.expected_salary_range_inr_lpa.max} LPA</p>
                            </div>
                            <div class="signal-card">
                                <h6>Work Mode</h6>
                                <p style="font-size: 0.85rem; text-transform: capitalize;">${cand.redrob_signals.preferred_work_mode}</p>
                            </div>
                            <div class="signal-card">
                                <h6>Profile Complete</h6>
                                <p>${cand.redrob_signals.profile_completeness_score.toFixed(0)}%</p>
                            </div>
                        </div>
                    </div>
                </div>

                <h3 class="section-title">Skills & Proficiencies</h3>
                <div class="skills-grid">${skillsHtml}</div>
            `;
        }

        // Initialize
        populateList(candidates);
        if (candidates.length > 0) {
            selectCandidate(candidates[0].candidate_id);
        }
    </script>
</body>
</html>
"""
    # URL encode the json to fit inside javascript string safely
    import urllib.parse
    json_data = urllib.parse.quote(json.dumps(sorted_details))
    
    html_content = html_template.replace("CANDIDATE_DATA_PLACEHOLDER", json_data)
    
    with open("dashboard.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print("dashboard.html generated successfully!")

if __name__ == "__main__":
    main()
