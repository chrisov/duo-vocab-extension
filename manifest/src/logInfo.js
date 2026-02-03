// console.log('[DUO-EXT] logInfo.js loaded');

// Track lesson clicks
function trackLessonClick(event) {
    const button = event.target.closest('button[data-test*="skill-path-level"]');
    if (!button) return;

    const dataTest = button.getAttribute('data-test') || '';
    const match = dataTest.match(/skill-path-level-(\d+)/);
    if (!match) return;

    const levelNumber = match[1];
    const skillPathSection = button.closest('[data-test^="skill-path-unit"]');
    const unitMatch = skillPathSection?.getAttribute('data-test')?.match(/skill-path-unit-(\d+)/);
    const unitNumber = unitMatch ? unitMatch[1] : 'unknown';

    // Extract language from page title (e.g., "Learn Spanish with lessons")
    const titleText = document.title || '';
    const languageMatch = titleText.match(/Learn (\w+) with/);
    const language = languageMatch ? languageMatch[1] : 'Unknown';

    const payload = {
        type: 'lesson_click',
        unit: unitNumber,
        level: levelNumber,
        language: language,
        timestamp: new Date().toISOString()
    };

    fetch('http://localhost:5000/log-lesson', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .catch(err => console.error("Error logging lesson:", err));
}