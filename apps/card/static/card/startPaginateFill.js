function createElement(currentPage, innerText,
                       disable = false, active = false) {
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
    pagination.innerHTML = ''

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
    pagination.innerHTML = ''

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
    pagination.innerHTML = ''
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

function fill(data) {
    const cards = document.getElementById('cards');
    cards.innerHTML = '';

    for (let item of data) {
        const name = item['name'].replaceAll(' ', '-');

        const card = document.createElement('section');
        card.className = `card ${name}`;

        const row = document.createElement('div');
        row.className = 'row';

        const cardImg = document.createElement('img');
        cardImg.className = 'card-img';
        cardImg.src = item['image_url'];
        cardImg.alt = `${name}`;
        cardImg.height = 150;
        row.append(cardImg);

        const container = document.createElement('div');
        container.className = 'container';

        const cardTitles = document.createElement('div');
        cardTitles.className = 'card-titles';

        const cardTitle = document.createElement('h2');
        cardTitle.className = 'card-title';
        cardTitle.innerText = item['name'];

        const cardSubtitle = document.createElement('h3');
        cardSubtitle.className = 'card-subtitle';
        cardSubtitle.innerText = item['type'];

        cardTitles.append(cardTitle);
        cardTitles.append(cardSubtitle);

        container.append(cardTitles);
        row.append(container);
        card.append(row);

        const rowContent = document.createElement('div');
        rowContent.className = 'row';

        const colContent = document.createElement('div');
        colContent.className = 'col';

        const collapsible = document.createElement('button');
        collapsible.className = `${name} collapsible`;
        collapsible.innerText = '6 star stats / details';
        colContent.append(collapsible);

        const content = document.createElement('div');
        content.className = `content ${name}`;
        content.id = name;

        const ul = document.createElement('ul');
        ul.className = 'lines-list';

        for (let i = 1; i < 7; i++) {
            const li = document.createElement('li');
            li.className = 'tab-text-text';
            li.innerHTML = item[`stat_${i}`];
            li.style.listStyleType = `'${i}★'`;
            ul.append(li);
        }
        content.append(ul);
        colContent.append(content);
        rowContent.append(colContent);
        card.append(rowContent);

        cards.append(card);
    }
}

function exec() {
        const coll = document.getElementsByClassName("collapsible");
        for (let j = 0; j < coll.length; j++) {
            coll[j].addEventListener("click", function() {
                this.classList.toggle("active-toggle");
                const content = this.nextElementSibling;
                if (content.style.maxHeight){
                    content.style.maxHeight = null;
                    content.style.padding = "0px 2rem";
                }
                else {
                    content.style.maxHeight = "60rem";
                    content.style.padding = "2rem";
                }
            });
        }
}

function run(currentPage, arg = null) {
    key = (arg) ? arg : '';

    fetch(APILink+key+'&page='+currentPage)
        .then(response => response.json())
        .then(data => {
            paginate(currentPage, data['count']);
            fill(data['results']);
            exec();
        });
}

var key;
const APILink = 'http://127.0.0.1:8000/api/card/search/?Key=';
const pagination = document.getElementById("pagination");
run(1);
