const close = () => {
    const bgShadow = document.getElementById('background-modal');
    const modal = document.getElementById('modal');

    bgShadow.style.display = 'none';
    bgShadow.style.opacity = '0';
    modal.style.display = 'none';
    modal.style.opacity = '0';
}

function startFill(data) {
    document.getElementById('modal-name').innerText = data.name;
    document.getElementById('modal-uniform').innerText = data.uniform;
    document.getElementById('modal').scrollTo(0, 0)

    const basics = document.getElementById('basics');
    basics.innerHTML = '';
    for (let item of [data.type, data.allies, data.gender, data.side]) {
        const div = document.createElement('div');
        div.className = 'modal-item';

        const img = document.createElement('img');
        img.className = 'modal-item-image';
        img.src = `/media/icons/Basics/${item}.png`

        const p = document.createElement('p');
        p.className = 'modal-item-text';
        p.innerText = item;

        div.append(img);
        div.append(p);
        basics.append(div);
    }

    const ability = document.getElementById('ability');
    ability.innerHTML = '';
    const abilities = JSON.parse(data.ability.replaceAll("'", '"'));

    ability.style.gridTemplateColumns = (abilities.length === 1) ? '10rem': '10rem 10rem';

    for (let item of abilities) {
        const div = document.createElement('div');
        div.className = 'modal-item';

        const img = document.createElement('img');
        img.className = 'modal-item-image';
        img.src = `/media/icons/Ability/${item}.png`

        const p = document.createElement('p');
        p.className = 'modal-item-text';
        p.innerText = item;

        div.append(img);
        div.append(p);
        ability.append(div);
    }

    const advancement = document.getElementById('advancement');
    advancement.innerHTML = '';
    advancement.style.gridTemplateColumns = '10rem';
    let div = document.createElement('div');
    div.className = 'modal-item';

    let img = document.createElement('img');
    img.className = 'modal-item-image';
    img.src = `/media/icons/Advancement/${data.advancement}.png`

    let p = document.createElement('p');
    p.className = 'modal-item-text';
    p.innerText = data.advancement;

    div.append(img);
    div.append(p);
    advancement.append(div);

    const instinct = document.getElementById('instinct');
    instinct.innerHTML = '';
    instinct.style.gridTemplateColumns = '10rem';
    p = document.createElement('p');
    p.className = 'modal-item-text';
    p.innerText = data.instinct;
    instinct.append(p);
}

function fillDetailCharacter (id) {
    fetch('http://127.0.0.1:8000/api/character/retrieve/'+id)
        .then(response => response.json())
        .then(data => {
            startFill(data)
        });
}

function modalPopUp (id) {
    const bgShadow = document.getElementById('background-modal');
    const modal = document.getElementById('modal');
    const closeBtn = document.getElementById('modal-close');

    bgShadow.style.display = 'block';
    bgShadow.style.opacity = '0.5';
    modal.style.display = 'block';
    modal.style.opacity = '1';

    bgShadow.onclick = close;
    closeBtn.onclick = close;

    fillDetailCharacter(id)
}