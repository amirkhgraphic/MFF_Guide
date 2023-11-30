function createElement(currentPage, innerText, disable = false, active = false) {
    let btn = document.createElement('button');
    btn.className = (innerText === '...') ? '' : (active) ? 'active' : 'button-hover';
    btn.disabled = disable;
    btn.innerText = innerText;
    btn.onclick = (disable) ? null
        : (innerText === "«") ? () => run(currentPage - 1, key)
        : (innerText === "»") ? () => run(currentPage + 1, key)
        : () => run(innerText, key);
    return btn;
}

function paginateFirst3 (pagesNumber, currentPage) {
    if (currentPage === 1) pagination.append(createElement(currentPage, '«', true));
    else pagination.append(createElement(currentPage, '«'));
    for (let i of [1, 2, 3]) {
        if (i === currentPage) pagination.append(createElement(currentPage, i, true, true));
        else pagination.append(createElement(currentPage, i));
    }
    pagination.append(createElement(currentPage, `...`, true));
    pagination.append(createElement(currentPage, pagesNumber-2));
    pagination.append(createElement(currentPage, pagesNumber-1));
    pagination.append(createElement(currentPage, pagesNumber));
    pagination.append(createElement(currentPage, '»'));

}

function paginateLast3 (pagesNumber, currentPage) {
    pagination.append(createElement(currentPage, '«'));
    pagination.append(createElement(currentPage, 1));
    pagination.append(createElement(currentPage, 2));
    pagination.append(createElement(currentPage, 3));
    pagination.append(createElement(currentPage, `...`, true));

    for (let i= pagesNumber-2; i <= pagesNumber; i++) {
        if (i === currentPage) pagination.append(createElement(currentPage, i, true, true));
        else pagination.append(createElement(currentPage, i));
    }
    if (currentPage === pagesNumber) pagination.append(createElement(currentPage, '»', true));
    else pagination.append(createElement(currentPage, '»'));
}

function paginateBetween (pagesNumber, currentPage) {
    pagination.append(createElement(currentPage, '«'));
    pagination.append(createElement(currentPage, 1));
    pagination.append(createElement(currentPage, 2));
    pagination.append(createElement(currentPage, `...`, true));
    pagination.append(createElement(currentPage, currentPage, true, true));
    pagination.append(createElement(currentPage, `...`, true));
    pagination.append(createElement(currentPage, pagesNumber-1));
    pagination.append(createElement(currentPage, pagesNumber));
    pagination.append(createElement(currentPage, '»'));
}

function paginate(currentPage, count) {
    const pagesNumber = Math.ceil(count / 20);
    pagination.innerHTML = '';

    if (7 <= pagesNumber) {

        if (currentPage <= 3) paginateFirst3(pagesNumber, currentPage);
        else if (pagesNumber-2 <= currentPage) paginateLast3(pagesNumber, currentPage);
        else paginateBetween(pagesNumber, currentPage)
    }
    else {

        if (currentPage === 1) pagination.append(createElement(currentPage, '«', true));
        else pagination.append(createElement(currentPage, '«'));

        for (let i= 1; i <= pagesNumber; i++) {
            if (i === currentPage) pagination.append(createElement(currentPage, i, true, true));
            else pagination.append(createElement(currentPage, i));
        }

        if (currentPage === pagesNumber) pagination.append(createElement(currentPage, '»', true));
        else pagination.append(createElement(currentPage, '»'));
    }
}

function changeTab(e, name, rank) {
    const tabContent = document.getElementsByClassName(`tab-content ${name}`);
    for (let i = 0; i < tabContent.length; i++) {
      tabContent[i].style.display = "none";
    }
    document.getElementById(name+"-"+rank).style.display = "block";

    const tabLinks = document.getElementsByClassName(`tab-links ${name}`);
    for (let i = 0; i < tabLinks.length; i++) {
      tabLinks[i].className = tabLinks[i].className.replace(" active", "");
    }
    e.currentTarget.className += " active";
}

function fill(data) {
    const cards = document.getElementById('cards');
    cards.innerHTML = '';

    for (let item of data) {
        const name = item['name'].replaceAll(' ', '-');

        const card = document.createElement('section');
        card.className = `card ${name}`;

        const row = document.createElement('div');
        row.className = 'row-artifact';

        const cardImg = document.createElement('img');
        cardImg.className = 'card-img';
        cardImg.src = item['image_url'];
        cardImg.alt = `${name}`;
        cardImg.width = 150;
        cardImg.height = 150;
        row.append(cardImg);

        const container = document.createElement('div');
        container.className = 'container row';

        const colName = document.createElement('div');
        colName.className = 'col-artifact';
        const nameSubtitle = document.createElement('h3');
        nameSubtitle.className = 'artifact-subtitle';
        nameSubtitle.innerText = 'artifact name';
        const nameTitle = document.createElement('h2');
        nameTitle.className = 'artifact-title';
        nameTitle.innerText = item['name'];
        colName.append(nameSubtitle);
        colName.append(nameTitle);

        const colCharacter = document.createElement('div');
        colCharacter.className = 'col-artifact';
        const characterSubtitle = document.createElement('h3');
        characterSubtitle.className = 'artifact-subtitle';
        characterSubtitle.innerText = 'character name';
        const characterTitle = document.createElement('h2');
        characterTitle.className = 'artifact-title';
        characterTitle.innerText = item['character_name'];
        colCharacter.append(characterSubtitle);
        colCharacter.append(characterTitle);

        const colSkill = document.createElement('div');
        colSkill.className = 'col-artifact';
        const skillSubtitle = document.createElement('h3');
        skillSubtitle.className = 'artifact-subtitle';
        skillSubtitle.innerText = 'exclusive skill';
        const skillTitle = document.createElement('h2');
        skillTitle.className = 'artifact-title';
        skillTitle.innerText = item['exclusive_skill'];
        colSkill.append(skillSubtitle);
        colSkill.append(skillTitle);

        container.append(colName);
        container.append(colCharacter);
        container.append(colSkill);
        row.append(container);

        const rowScore = document.createElement('div');
        rowScore.className = 'row-artifact score';

        const PvPScore = document.createElement('div');
        PvPScore.className = 'col-artifact pvp-score'

        const PvPTitle = document.createElement('p');
        PvPTitle.className = 'score-title';
        PvPTitle.innerText = 'PvP Score';
        PvPScore.append(PvPTitle);

        const PvPScoreContent = document.createElement('div');
        PvPScoreContent.className = 'row-artifact score-content row-direction';

        const low = document.createElement('div');
        low.className = 'low';
        PvPScoreContent.append(low);

        if (item['PvP_score'] === 'Medium') {
            const medium = document.createElement('div');
            medium.className = 'medium';
            const high = document.createElement('div');
            high.className = 'high empty';
            PvPScoreContent.append(medium);
            PvPScoreContent.append(high);
        }
        else if (item['PvP_score'] === 'High') {
            const medium = document.createElement('div');
            medium.className = 'medium';
            const high = document.createElement('div');
            high.className = 'high';
            PvPScoreContent.append(medium);
            PvPScoreContent.append(high);
        }
        else {
            const medium = document.createElement('div');
            medium.className = 'medium empty';
            const high = document.createElement('div');
            high.className = 'high empty';
            PvPScoreContent.append(medium);
            PvPScoreContent.append(high);
        }
        PvPScore.append(PvPScoreContent);

        const PvEScore = document.createElement('div');
        PvEScore.className = 'col-artifact pve-score';

        const PvETitle = document.createElement('p');
        PvETitle.className = 'score-title';
        PvETitle.innerText = 'PvE Score';
        PvEScore.append(PvETitle);

        const PvEscoreContent = document.createElement('div');
        PvEscoreContent.className = 'row-artifact score-content row-direction';
        const PvElow = document.createElement('div');
        PvElow.className = 'low';
        PvEscoreContent.append(PvElow);

        if (item['PvE_score'] === 'Medium') {
            const medium = document.createElement('div');
            medium.className = 'medium';
            const high = document.createElement('div');
            high.className = 'high empty';

            PvEscoreContent.append(medium);
            PvEscoreContent.append(high);
        }
        else if (item['PvE_score'] === 'High') {
            const medium = document.createElement('div');
            medium.className = 'medium';
            const high = document.createElement('div');
            high.className = 'high';

            PvEscoreContent.append(medium);
            PvEscoreContent.append(high);
        }
        else {
            const medium = document.createElement('div');
            medium.className = 'medium empty';
            const high = document.createElement('div');
            high.className = 'high empty';
            PvEscoreContent.append(medium);
            PvEscoreContent.append(high);
        }
        PvEScore.append(PvEscoreContent);

        rowScore.append(PvPScore);
        rowScore.append(PvEScore);

        const rowRank = document.createElement('div');
        rowRank.className = 'row-artifact rank';

        const colRank = document.createElement('div');
        colRank.style.width = '100%';
        colRank.style.textAlign = 'start';

        const tabs = document.createElement('div');
        tabs.className = 'tab';

        for (let i = 3; i < 7; i++) {
            const rankBtn = document.createElement('button');
            rankBtn.onclick = () => changeTab(event, name, `${i}`);
            rankBtn.className = (i === 3) ? `tab-links ${name} active` : `tab-links ${name}`;
            rankBtn.innerText = '★'.repeat(i);
            tabs.append(rankBtn)
        }
        colRank.append(tabs)

        for (let i = 3; i < 7; i++) {
            const tabContent = document.createElement('div');
            tabContent.className = (i === 3) ? `tab-content ${name} show` : `tab-content ${name}`;
            tabContent.id = `${name}-${i}`;

            const ul = document.createElement('ul');
            ul.className = 'lines-list';

            let lines = item[`rank_${i}`].split('\n').map(item => item.trim().replace('•', '').trim());

            for (let line of lines) {
                const li = document.createElement('li');
                li.className = 'tab-text-text';
                li.innerText = line;
                ul.append(li);
            }

            tabContent.append(ul);
            colRank.append(tabContent);
        }
        rowRank.append(colRank)

        card.append(row);
        card.append(rowScore);
        card.append(rowRank);
        cards.append(card)
    }
}

function run(currentPage, arg = null) {
    key = (arg) ? arg : '';

    fetch(APILink+key+'&page='+currentPage)
        .then(response => response.json())
        .then(data => {
            paginate(currentPage, data['count']);
            fill(data['results']);
        });
}

var key;
const APILink = 'http://127.0.0.1:8000/api/artifact/search/?Key=';
const pagination = document.getElementById("pagination");
run(1);