function changeTab (e, name, rank) {
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

function fill(data, count) {
    const cards = document.getElementById('cards');
    cards.innerHTML = '';
    
    let i = 0;
    while (i < count) {
        const name = data[i]['name'].split(' ')[2];

        const card = document.createElement('section');
        card.className = `card ${name}`;

        const row = document.createElement('div');
        row.className = 'row';

        const cardImg = document.createElement('img');
        cardImg.className = 'card-img';
        cardImg.src = data[i]['image_url'];
        cardImg.alt = name;
        cardImg.width = 150;
        cardImg.height = 150;
        row.append(cardImg);

        const container = document.createElement('div');
        container.className = 'container';

        const cardTitles = document.createElement('div');
        cardTitles.className = 'card-titles';

        const cardTitle = document.createElement('h2');
        cardTitle.className = 'card-name';
        cardTitle.innerText = data[i]['name'];

        cardTitles.append(cardTitle);
        container.append(cardTitles);
        row.append(container);
        card.append(row);

        const cardText = document.createElement('div');
        cardText.className = 'card-text';

        const description1 = document.createElement('div');
        description1.className = 'description';

        const head1 = document.createElement('h4');
        head1.className = 'card-text-title head-normal';
        head1.innerText = 'DESCRIPTION';

        const p1 = document.createElement('p');
        p1.className = 'card-text-text text-normal';
        p1.innerText = data[i]['description'];

        description1.append(head1);
        description1.append(p1);
        cardText.append(description1);

        const description2 = document.createElement('div');
        description2.className = 'description';

        const head2 = document.createElement('h4');
        head2.className = 'card-text-title head-normal';
        head2.innerText = 'REFORGED DESCRIPTION';

        const p2 = document.createElement('p');
        p2.className = 'card-text-text text-normal';
        p2.innerText = data[i]['reforged_description'];

        description2.append(head2);
        description2.append(p2);
        cardText.append(description2);

        container.append(cardText);

        const row2 = document.createElement('div');
        row2.className = 'row';

        const col = document.createElement('div');
        col.className = 'col';

        const tabLinks = document.createElement('div');
        tabLinks.className = 'tab';

        for (let status of ['Regular', 'Mighty', 'Brilliant']) {
            const tabLink = document.createElement('button');
            tabLink.className = (status === 'Regular') ? `tab-links ${name} active` : `tab-links ${name}`;
            tabLink.onclick = () => changeTab(event, name, status);
            tabLink.innerText = status;
            tabLinks.append(tabLink);
        }
        col.append(tabLinks);

        for (let status of ['Regular', 'Mighty', 'Brilliant']) {
            const tabContent = document.createElement('div');
            tabContent.className = (status === 'Regular') ? `tab-content ${name} show` : `tab-content ${name}`;
            tabContent.id = `${name}-${status}`;

            const italic = document.createElement('i');
            const header4 = document.createElement('h4');
            header4.className = 'tab-text-title';
            header4.innerText = 'MAX STATS:';
            italic.append(header4)

            const ul = document.createElement('ul');
            ul.className = 'lines-list';

            for (let item of data[i]['max_stats'].split('\n')) {
                const li = document.createElement('li');
                li.className = 'tab-text-text';
                li.innerHTML = item;
                ul.append(li);
            }
            tabContent.append(italic);
            tabContent.append(ul);

            if (status === 'Mighty' || status === 'Brilliant') {
                const italic2 = document.createElement('i');
                const header42 = document.createElement('h4');
                header42.className = 'tab-text-title';
                header42.innerText = 'REFORGED STATS:';
                italic2.append(header42)

                const ul2 = document.createElement('ul');
                ul2.className = 'lines-list';

                for (let item of data[i]['reforged_option_1'].split('\n')) {
                    const li = document.createElement('li');
                    li.className = 'tab-text-text';
                    li.innerHTML = item;
                    ul2.append(li);
                }

                tabContent.append(italic2);
                tabContent.append(ul2);

                const italicOR = document.createElement('i');
                const header4OR = document.createElement('h4');
                header4OR.className = 'tab-text-title';
                header4OR.innerText = 'OR';
                italicOR.append(header4OR);

                const ulOR = document.createElement('ul');
                ulOR.className = 'lines-list';

                for (let item of data[i]['reforged_option_2'].split('\n')) {
                    const li = document.createElement('li');
                    li.className = 'tab-text-text';
                    li.innerHTML = item;
                    ulOR.append(li);
                }

                tabContent.append(italicOR);
                tabContent.append(ulOR);
            }

            col.append(tabContent)
            i++;
        }

        row2.append(col);
        card.append(row2);

        cards.append(card);
    }
}

function run(currentPage, arg = null) {
    key = (arg) ? arg : '';

    fetch(APILink+key+'&page='+currentPage)
        .then(response => response.json())
        .then(data => fill(data['results'], data['count']));
}

var key;
const APILink = 'http://127.0.0.1:8000/api/ctp/search/?Key=';
run(1);
