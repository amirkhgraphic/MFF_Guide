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
        const uniform = item['uniform'].replaceAll(' ', '-');
        const rotations = item['rotation'];

        const card = document.createElement('section');
        card.className = `card ${name}-${uniform}`;

        const row = document.createElement('div');
        row.className = 'row';

        const cardImg = document.createElement('img');
        cardImg.className = 'card-img';
        cardImg.src = item['image_url'];
        cardImg.alt = `${name}-${uniform}`;
        cardImg.width = 150;
        cardImg.height = 150;
        cardImg.onclick = () => modalPopUp(item['id'])

        const container = document.createElement('div');
        container.className = 'container';

        const cardTitle = document.createElement('div');
        cardTitle.className = 'card-title';

        const cardName = document.createElement('h2');
        cardName.className = 'card-name';
        cardName.innerText = item['name'];

        const cardUniform = document.createElement('h3');
        cardUniform.className = 'card-uniform';
        cardUniform.innerText = item['uniform'];

        const cardText = document.createElement('div');
        cardText.className = 'card-text';

        if (rotations) {
            Object.entries(rotations).forEach((key) => {
                const rotation = document.createElement('div');
                rotation.className = 'rotation';

                const rotationName = document.createElement('h4');
                rotationName.className = 'rotation-name';
                rotationName.innerText = key[0];

                const rotationText = document.createElement('p');
                rotationText.className = 'rotation-text';
                rotationText.innerText = key[1];

                rotation.append(rotationName);
                rotation.append(rotationText);
                cardText.append(rotation);
            });
        } else {
            const rotation = document.createElement('div');
            rotation.className = 'rotation';

            const rotationText = document.createElement('p');
            rotationText.className = 'rotation-text';
            rotationText.innerText = 'Rotations(s) for this character/uniform have not been added yet.';

            rotation.append(rotationText);
            cardText.append(rotation);

        }

        cardTitle.append(cardName);
        cardTitle.append(cardUniform);
        container.append(cardTitle);
        container.append(cardText)
        row.append(cardImg);
        row.append(container);
        card.append(row);
        cards.append(card);
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
const APILink = 'http://127.0.0.1:8000/api/character/search/?Key=';
const pagination = document.getElementById("pagination");
run(1);
