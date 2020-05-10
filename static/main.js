let from = null;
let waiting = false;
let previousRows = null;

function createChessboard() {
    const parent = document.getElementById('squares');

    for (let row = 0; row < 8; row++) {
        const tr = document.createElement('tr');
        tr.className = 'row';
        parent.append(tr);

        for (let col = 0; col < 8; col++) {
            const td = document.createElement('td');
            td.className = 'square';
            td.dataset.position = position(row, col);
            tr.append(td);

            const button = document.createElement('button');
            button.className = 'square-button';
            button.dataset.position = position(row, col);
            td.append(button);

            const positionLabel = document.createElement('span');
            positionLabel.className = 'position-label';
            positionLabel.textContent = position(row, col);
            button.append(positionLabel);

            button.onclick = async () => {
                if (from === null) {
                    from = button;
                    from.classList.add('from');
                }
                else if (from === button) {
                    from.classList.remove('from');
                    from = null;
                }
                else {
                    waiting = true;
                    button.classList.add('to');
                    const buttons = Array.from(document.querySelectorAll('.square-button'));
                    buttons.forEach(b => b.disabled = true);
                    try {
                        await makeMove(from.dataset.position, button.dataset.position);
                    }
                    finally {
                        buttons.forEach(b => b.disabled = false);
                        from.classList.remove('from');
                        button.classList.remove('to');
                        from = null;
                        waiting = false;
                    }
                }
                
                button.blur();
            };
        }
    }

    document.onclick = event => {
        if (waiting) return;

        if (!parent.contains(event.target) && from !== null) {
            from.classList.remove('from');
            from = null;
        }
    };
}

function position(row, col) {
    const letter = String.fromCharCode(65 + col);
    const number = 8 - row;
    return letter + number;
}

function fillChessboard(rows) {
    if (!Array.isArray(rows)) {
        throw new Error('Board has wrong data type: ' + typeof rows + ' instead of array');
    }

    if (rows.length != 8) {
        throw new Error('Board has wrong number of rows: ' + rows.length + ' instead of 8');
    }

    rows.forEach((row, rowIndex) => {
        if (!Array.isArray(row)) {
            throw new Error('Row with index ' + rowIndex + ' has wrong data type: ' + typeof row + ' instead of array.');
        }

        if (row.length != 8) {
            throw new Error('Row with index ' + rowIndex + ' has wrong number of columns: ' + row.length + ' instead of 8.');
        }
    });

    try {
        const images = Array.from(document.querySelectorAll('img.piece'));
        images.forEach(img => img.remove());
        
        const parent = document.getElementById('squares');
        for (let row = 0; row < 8; row++) {
            for (let col = 0; col < 8; col++) {
                const shorthand = rows[row][col];
                if (shorthand !== null) {
                    const img = document.createElement('img');
                    img.classList.add('piece');
                    img.classList.add(pieceColor(shorthand));
                    img.classList.add(pieceName(shorthand));
                    img.src = '/static/images/' + pieceName(shorthand) + '.svg';
                    parent.children[row].children[col].firstChild.append(img);
                }
            }
        }

        previousRows = rows;
    }
    catch(error) {
        if (previousRows !== null) {
            fillChessboard(previousRows);
        }
        throw error;
    }
}

function pieceName(shorthand) {
    if (typeof shorthand !== 'string') throw new Error('Piece has invalid data type: ' + typeof shorthand + ' instead of string');
    if (shorthand.length != 2) throw new Error('Piece string does not consist of exactly 2 characters: ' + shorthand);

    const name = {
        'p': 'pawn',
        'r': 'rook',
        'h': 'horse',
        'b': 'bishop',
        'q': 'queen',
        'k': 'king'
    }[shorthand[0]];

    if (typeof name !== 'string') {
        throw new Error('Not a valid piece name: ' + shorthand[0]);
    }

    return name;
}

function pieceColor(shorthand) {
    if (typeof shorthand !== 'string') throw new Error('Piece has invalid data type: ' + typeof shorthand + ' instead of string');
    if (shorthand.length != 2) throw new Error('Piece string does not consist of exactly 2 characters: ' + shorthand);
    
    const color = {
        'b': 'black',
        'w': 'white',
    }[shorthand[1]];

    if (typeof color !== 'string') {
        throw new Error('Not a valid color: ' + shorthand[1]);
    }

    return color;
}

async function makeMove(from, to) {
    let response = null;
    try {
        response = await fetch(location.origin + '/move?from=' + from + '&to=' + to, {
            method: 'POST'
        });
    }
    catch(error) {
        showMessage('Network error: ' + error.message);
    }

    if (response !== null) await handleResponse(response, 'Latest move: ' + from + ' to ' + to);
}

async function handleResponse(response, message) {
    if (response.ok) {
        try {
            const state = await response.json();
            showMessage(message);
            handleNewState(state);
        }
        catch(error) {
            showMessage('Error: ' + error.message);
        }
    }
    else {
        const text = await response.text();
        showMessage('Error: ' + text);
    }
}

function handleNewState(state) {
    document.getElementById('player-color').textContent = capitalize(state.player);
    fillChessboard(state.board);
    if (state.latest_to_square) {
        highlightSquares([state.latest_from_square, state.latest_to_square]);
    }
}

function showMessage(text) {
    document.getElementById('message').textContent = text;
}

function onShowPositionsChange(show) {
    document.documentElement.classList.toggle('show-positions', show);
}

function capitalize(text) {
    return text[0].toUpperCase() + text.slice(1);
}

function highlightSquares(positions) {
    const squares = Array.from(document.querySelectorAll('.square'));
    squares.forEach(square => {
        if (positions.includes(square.dataset.position)) {
            square.classList.add('highlighted');
        }
        else {
            square.classList.remove('highlighted');
        }
    })
}

async function start() {
    createChessboard();

    let response = null;
    try {
        response = await fetch(location.origin + '/state');
    }
    catch(error) {
        showMessage('Network error: ' + error.message);
    }

    if (response !== null) await handleResponse(response, 'Welcome!');

    const pollFrequency = 1000;
    let latestPoll = Date.now() / 1000;
    setTimeout(async function poll() {
        const timestamp = Date.now() / 1000;
        const response = await fetch(location.origin + '/state?since=' + latestPoll);
        try {
            if (response.ok && response.status !== 304) {
                const state = await response.json();
                handleNewState(state);
            }
        }
        finally {
            setTimeout(poll, pollFrequency);
        }
        latestPoll = timestamp;
    }, pollFrequency);
}

start();