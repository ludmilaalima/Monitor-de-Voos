const btnReload = document.getElementById('btnReload');
const tableBody = document.querySelector('#listMonitor tbody');

async function loadMonitors(){
    try{
        tableBody.innerHTML = '<tr><td colspan="6">Carregando</td></tr>'
        const response = await fetch('/api/monitors');
        if (!response.ok){
            throw new Error(`Erro HTTP: ${response.status}`);

        }
        const monitors = await response.json()
        tableBody.innerHTML = '';
        if (monitors.length === 0){
            tableBody.innerHTML = '<tr><td colspan="6">Nenhum monitor cadastrado ainda</td></tr>';
            return
        }

        monitors.forEach(function(monitor){
            const tr = document.createElement('tr')
            tr.innerHTML=`
            <td>${monitor.id}</td>
            <td>${monitor.origin_iata}</td>
            <td>${monitor.destination_iata}</td>
            <td>${monitor.frequency}</td>
            <td>${monitor.status}</td>
            <td>${monitor.lowest_price ?? '-'}</td>
            `;
            tableBody.appendChild(tr); 
    
        });

    } catch (error){
        console.error('Erro ao carregar monitores:', error);
        tableBody.innerHTML = '<tr><td colspan="6">Erro ao carregar monitores</td></tr>';
    }}

    btnReload.addEventListener('click', loadMonitors);

loadMonitors();



    
   