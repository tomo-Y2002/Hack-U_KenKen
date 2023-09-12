'use strict';

const record1=['2023/09/11 17:03:30', '見附昂紀'];
const record2=['2023/09/11 17:04:30', '出分寛人'];

const table = document.getElementById('record-table')

// 表の要素追加
const appendRecord = (record) => {
    const tr = document.createElement('tr');
    tr.className = 'record-row'
    for (const data of record){
        console.log(data);
        const td = document.createElement('td');
        td.textContent=data;
        tr.appendChild(td)
    }
    table.appendChild(tr);
}

appendRecord(record2);
appendRecord(record2);
appendRecord(record1);
appendRecord(record1);
appendRecord(record1);
appendRecord(record1);
appendRecord(record2);
appendRecord(record2);
appendRecord(record2);
appendRecord(record2);
appendRecord(record2);
appendRecord(record2);
appendRecord(record2);
appendRecord(record2);
appendRecord(record2);

// 表の初期化
const deleteRecord = () => {
    var clone = table.cloneNode(false);
    createTable(clone);
    table.parentNode.replaceChild(clone, table);
    console.log('aa');
}

// 初期化の際の1列目(通過日時,名前)作成
const createTable = (table) => {
    const tr = document.createElement('tr');
    for (let i = 0; i < 2; i++){
        const th = document.createElement('th');
        if (i == 0){
            th.textContent='通過日時';
        }
        else{
            th.textContent='名前';
        }
        tr.appendChild(th);
    }
    table.appendChild(tr);
}

// deleteRecord();
