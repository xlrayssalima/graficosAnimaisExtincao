async function init() {
    const cardsContainer = document.getElementById('cards');
    const categoriasContainer = document.getElementById('categorias');
    const especiesContainer = document.getElementById('especies');
    const graficosContainer = document.getElementById('graficos');
    const buscaInput = document.getElementById('busca');

    try {
        const response = await fetch('data/dashboard.json');
        if (!response.ok) throw new Error(`Erro: ${response.status}`);
        const d = await response.json();

        window.bancoEspeciesRisco = d.especies_risco || {};

        // 1. Cards de Métricas
        if (cardsContainer) {
            cardsContainer.innerHTML = `
                <div class="col-md-4">
                    <div class="card metric-card border-0 border-start border-primary border-4 shadow-sm bg-white p-4">
                        <span class="text-muted text-uppercase small fw-bold">Total de Espécies</span>
                        <h2 class="display-6 fw-bold text-dark mt-1 mb-0">${d.total_especies || 0}</h2>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card metric-card border-0 border-start border-success border-4 shadow-sm bg-white p-4">
                        <span class="text-muted text-uppercase small fw-bold">Grupos Taxonômicos</span>
                        <h2 class="display-5 fw-bold text-dark mt-1 mb-0">${d.total_grupos || 0}</h2>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card metric-card border-0 border-start border-danger border-4 shadow-sm bg-white p-4">
                        <span class="text-muted text-uppercase small fw-bold">Categorias Avaliadas</span>
                        <h2 class="display-5 fw-bold text-dark mt-1 mb-0">${d.total_categorias || 0}</h2>
                    </div>
                </div>
            `;
        }

        // 2. Badges de Categorias
        if (categoriasContainer && d.categorias) {
            categoriasContainer.innerHTML = '';
            d.categorias.forEach(c => {
                if(c.length > 2) {
                    categoriasContainer.innerHTML += `<span class="badge badge-cat m-1">${c}</span>`;
                }
            });
        }

        // 3. Filtro de Espécies
        function renderEspecies(lista, termoBusca) {
            if (!especiesContainer) return;
            especiesContainer.innerHTML = '';
            
            if (!termoBusca || termoBusca.trim() === '') {
                especiesContainer.innerHTML = `
                    <div class="col-12 text-center py-4 text-muted">
                        <p class="mb-0">Digite o nome de uma espécie para filtrar os resultados da planilha.</p>
                    </div>`;
                return;
            }
            
            if (lista.length === 0) {
                especiesContainer.innerHTML = `<div class="col-12 text-muted ps-3 py-2">Nenhuma espécie correspondente encontrada.</div>`;
                return;
            }
            
            lista.slice(0, 24).forEach(e => {
                const risco = window.bancoEspeciesRisco[e] || "Ameaçada";
                especiesContainer.innerHTML += `
                    <div class="col-md-4">
                        <div class="card especie-card shadow-sm border-0 bg-white h-100">
                            <div class="card-body p-3 d-flex align-items-center justify-content-between">
                                <div class="overflow-hidden me-2">
                                    <div class="fw-semibold text-dark text-truncate mb-1">${e}</div>
                                    <span class="badge bg-danger-subtle text-danger rounded-pill px-2 py-1" style="font-size:0.75rem;">${risco}</span>
                                </div>
                                <button class="btn btn-sm btn-success rounded-circle px-2 flex-shrink-0" 
                                        onclick="buscarFichaEspecie('${e.replace(/'/g, "\\'")}')">
                                    ＋
                                </button>
                            </div>
                        </div>
                    </div>`;
            });
        }

        if (buscaInput && d.especies) {
            buscaInput.oninput = () => {
                const termo = buscaInput.value.toLowerCase();
                const filtrados = d.especies.filter(x => x.toLowerCase().includes(termo));
                renderEspecies(filtrados, termo);
            };
        }
        renderEspecies([], '');

        // 4. Renderização Limpa e Forçada Horizontalmente dos Gráficos (3 por linha)
        if (graficosContainer) {
            const exemplos = ['barra_anfibios.png', 'barra_aves.png', 'pizza_anfibios.png', 'pizza_aves.png'];
            graficosContainer.innerHTML = '';
            
            exemplos.forEach(g => {
                graficosContainer.innerHTML += `
                    <div class="col-md-4 mb-4">
                        <div class="card h-100 shadow-sm border-0 rounded-4 bg-white p-3 text-center">
                            <div class="d-flex align-items-center justify-content-center" style="min-height:240px; width:100%;">
                                <img src="graficos/${g}" class="img-fluid grafico rounded-3" alt="Gráfico" onerror="this.parentElement.innerHTML='<div class=\"text-muted small p-4\">Gráfico pendente: <code>${g}<code></div>'">
                            </div>
                        </div>
                    </div>`;
            });
        }

        document.addEventListener('click', e => {
            if (e.target.classList.contains('grafico')) {
                const imgModal = document.getElementById('imgModal');
                if (imgModal) {
                    imgModal.src = e.target.src;
                    new bootstrap.Modal(document.getElementById('imagemModal')).show();
                }
            }
        });

    } catch (error) {
        console.error("Erro na inicialização:", error);
    }
}

// MODAL SEM IMAGEM - APENAS COMPONENTES TÉCNICOS EXATOS
async function buscarFichaEspecie(nomeEspecie) {
    const modalTitulo = document.getElementById('detalheModalLabel');
    const modalCorpo = document.getElementById('detalheModalCorpo');
    
    const meuModal = new bootstrap.Modal(document.getElementById('detalheModal'));
    modalTitulo.innerText = nomeEspecie;
    modalCorpo.innerHTML = `
        <div class="text-center py-5">
            <div class="spinner-border text-success" role="status"></div>
            <p class="mt-2 text-muted">Consultando dados biológicos consolidados...</p>
        </div>`;
    meuModal.show();

    const riscoOficial = window.bancoEspeciesRisco[nomeEspecie] || "Status Conforme Legislação Federal";
    let taxonomia = { kingdom: 'Animalia', class: 'Não Informada', family: 'Não Informada', genus: 'Mapeado' };

    try {
        const resTaxon = await fetch(`https://api.gbif.org/v1/species/search?q=${encodeURIComponent(nomeEspecie)}&limit=1`).then(r => r.json());
        if (resTaxon.results && resTaxon.results.length > 0) {
            const taxonItem = resTaxon.results[0];
            taxonomia.kingdom = taxonItem.kingdom || taxonomia.kingdom;
            taxonomia.class = taxonItem.class || taxonomia.class;
            taxonomia.family = taxonItem.family || taxonomia.family;
            taxonomia.genus = taxonItem.genus || taxonomia.genus;
        }

        modalCorpo.innerHTML = `
            <div class="row g-3">
                <div class="col-12">
                    <div class="p-4 border border-danger-subtle bg-danger-light rounded-4 shadow-sm mb-2">
                        <h6 class="text-uppercase text-danger small fw-bold mb-1 tracking-wide">⚠️ Grau de Risco de Extinção</h6>
                        <p class="fs-3 fw-bold text-dark mb-0">${riscoOficial}</p>
                    </div>
                </div>
                <div class="col-12">
                    <div class="p-3 bg-light rounded-3">
                        <h6 class="text-uppercase text-muted small fw-bold mb-2">Classificação Taxonômica Oficial</h6>
                        <div class="row g-2 text-secondary small">
                            <div class="col-6"><strong>Reino:</strong> ${taxonomia.kingdom}</div>
                            <div class="col-6"><strong>Classe:</strong> ${taxonomia.class}</div>
                            <div class="col-6"><strong>Família:</strong> ${taxonomia.family}</div>
                            <div class="col-6"><strong>Gênero:</strong> ${taxonomia.genus}</div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="p-3 border border-light rounded-3 bg-light h-100">
                        <h6 class="text-uppercase text-muted small fw-bold mb-1">Localidade de Ocorrência</h6>
                        <p class="small mb-0 text-dark fw-medium">Nativo / Ocorrência no Território Brasileiro</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="p-3 border border-light rounded-3 bg-light h-100">
                        <h6 class="text-uppercase text-muted small fw-bold mb-1">Base de Dados Integrada</h6>
                        <p class="small mb-0 text-muted">Combinação das planilhas ICMBio/MMA com chaves globais do GBIF.</p>
                    </div>
                </div>
            </div>
        `;

    } catch (err) {
        modalCorpo.innerHTML = `
            <div class="p-4 border border-danger-subtle bg-danger-light rounded-4">
                <h6 class="text-uppercase text-danger small fw-bold mb-1">Status de Risco</h6>
                <p class="fs-3 fw-bold text-dark mb-0">${riscoOficial}</p>
            </div>`;
    }
}

document.addEventListener('DOMContentLoaded', init);

document.addEventListener('DOMContentLoaded',async ()=>{
try{
 const d=await fetch('data/dashboard.json').then(r=>r.json());

 const hero=document.querySelector('.hero');
 if(hero){
   const imgs=[
   'https://neomondo.org.br/w/wp-content/uploads/2018/08/arara-azul-neo-mondo.jpg',
   'https://revistaplaneta.com.br/wp-content/uploads/sites/3/2024/11/ararinha-azul.jpg',
   'https://static.nationalgeographicbrasil.com/files/styles/image_3200/public/02gambarini_779-24.webp?w=1600&h=900'];
   const img=imgs[Math.floor(Math.random()*imgs.length)];
   hero.style.background=`linear-gradient(rgba(15,23,42,.65),rgba(15,23,42,.8)),url(${img}) center/cover`;
 }

 const cat=document.getElementById('categorias');
 if(cat && d.especies_risco){
   const total=Object.keys(d.especies_risco).length;
   const cont={};
   Object.values(d.especies_risco).forEach(v=>cont[v]=(cont[v]||0)+1);
   cat.innerHTML='';
   Object.entries(cont).sort().forEach(([nome,q])=>{
      const p=((q/total)*100).toFixed(1);
      cat.innerHTML += `<span class="badge badge-cat">${nome}<span class="percentual-cat">${p}%</span></span>`;
   });
 }

 const g=document.getElementById('graficos');
 if(g){
   g.innerHTML='';

   const grupos = [
    {
      nome:'Anfíbios',
      icone:'https://cdn-icons-png.flaticon.com/512/3065/3065709.png ',
      graficos:[
        {titulo:'Distribuição por Categoria',arquivo:'barra_anfibios.png'},
        {titulo:'Participação das Categorias',arquivo:'pizza_anfibios.png'},
        {titulo:'Análise de Dispersão',arquivo:'dispersao_anfibios.png'}
      ]
    },
    {
      nome:'Aves',
      icone:'https://cdn-icons-png.flaticon.com/512/8277/8277557.png',
      graficos:[
        {titulo:'Distribuição por Categoria',arquivo:'barra_aves.png'},
        {titulo:'Participação das Categorias',arquivo:'pizza_aves.png'},
        {titulo:'Análise de Dispersão',arquivo:'dispersao_aves.png'}
      ]
    },
    {
      nome:'Invertebrados',
      icone:'https://cdn-icons-png.flaticon.com/512/8099/8099026.png',
      graficos:[
        {titulo:'Distribuição por Categoria',arquivo:'countplot_invertebrados.png'},
        {titulo:'Participação das Categorias',arquivo:'pizza_invertebrados.png'},
        {titulo:'Análise de Dispersão Invertebrados Marinhos e de Água Doce',arquivo:'dispersao_invertebrados.png'},
        {titulo:'Histograma - Invertebrados Terrestres por Ano',arquivo:'ritograma_invertebrados.png'},
        {titulo:'Histograma - Invertebrados Terrestres por Ano',arquivo:'pizza_invertebrados_terrestres.png'},
        {titulo:'Análise de Dispersão Invertebrados Terrestres',arquivo:'dispersao_invertebrados_terrestres.png'}
      ]
    },
    {
      nome:'Peixes Continentais',
      icone:'https://cdn-icons-png.flaticon.com/512/2969/2969965.png',
      graficos:[
        {titulo:'Distribuição por Categoria - 2026',arquivo:'histograma_peixes_continentais_2026.png'},
        {titulo:'Participação das Categorias - 2026',arquivo:'pizza_peixes_continentais_2026.png'}
      ]
    },
    {
      nome:'Peixes Marinhos',
      icone:'https://cdn-icons-png.flaticon.com/512/4971/4971939.png',
      graficos:[
        {titulo:'Distribuição por Categoria - 2026',arquivo:'histograma_peixes_marinhos_2026.png'},
        {titulo:'Participação das Categorias - 2026',arquivo:'pizza_peixes_marinhos_2026.png'}
      ]
    },
    {
      nome:'Mamiferos',
      icone:'https://cdn-icons-png.flaticon.com/512/2395/2395796.png',
      graficos:[
        {titulo:'Distribuição por Categoria',arquivo:'ritograma_mamiferos.png'},
        {titulo:'Dispersão por Categoria',arquivo:'dispersao_mamiferos.png'},
        {titulo:'Participação por Categoria',arquivo:'pizza_mamiferos.png'}
      ]
    },
    {
      nome:'Répteis',
      icone:'https://cdn-icons-png.flaticon.com/512/4215/4215181.png',
      graficos:[
        {titulo:'Distribuição por Categoria',arquivo:'barras_repteis_salve.png'},
        {titulo:'Dispersão das Categorias',arquivo:'dispersao_repteis_salve.png'},
        {titulo:'Participação das Categorias',arquivo:'pizza_repteis_salve.png'}
      ]
    },
    {
      nome:'Tubarões e raias',
      icone:'https://cdn-icons-png.flaticon.com/512/4972/4972168.png',
      graficos:[
        {titulo:'Distribuição por Categoria',arquivo:'barras_tubaroes_salve.png'},
        {titulo:'Dispersão das Categorias',arquivo:'dispersao_tubaroes_salve.png'},
        {titulo:'Participação das Categorias',arquivo:'pizza_tubaroes_salve.png'}
      ]
    }
   ];

   grupos.forEach((gr,i)=>{
      const principal = gr.graficos[0];

      g.innerHTML += `
      <div class="col-12">
       <div class="grupo-card">
        <div class="grupo-topo">
         <img src="${gr.icone}">
         <div><h3>${gr.nome}</h3><p class="text-muted mb-0">Clique para abrir a galeria completa</p></div>
        </div>
        <div class="grupo-grafico-principal">
         <img src="graficos/${principal.arquivo}" data-bs-toggle="modal" data-bs-target="#grupoModal${i}">
        </div>
       </div>
      </div>

      <div class="modal fade" id="grupoModal${i}" tabindex="-1">
       <div class="modal-dialog modal-dialog-centered modal-xl">
        <div class="modal-content modal-graficos">
         <div class="modal-header border-0">
          <div class="w-100 text-center">
           <h2 class="grafico-modal-titulo">${gr.nome}</h2>
           <p class="text-muted mb-0">Análise Estatística do Grupo</p>
          </div>
          <button class="btn-close position-absolute top-0 end-0 m-4" data-bs-dismiss="modal"></button>
         </div>

         <div class="modal-body">
          <div id="carousel${i}" class="carousel slide" data-bs-ride="false">
           <div class="carousel-inner">

            ${gr.graficos.map((graf,index)=>`
             <div class="carousel-item ${index===0?'active':''}">
              <img src="graficos/${graf.arquivo}" class="d-block w-100 grafico-modal-img">
              <div class="text-center mt-4">
               <h5 class="fw-bold">${graf.titulo}</h5>
               <small class="text-muted">${index + 1} de ${gr.graficos.length}</small>
              </div>
             </div>
            `).join('')}

           </div>

           <button class="carousel-control-prev" type="button" data-bs-target="#carousel${i}" data-bs-slide="prev">
            <span class="carousel-control-prev-icon"></span>
           </button>

           <button class="carousel-control-next" type="button" data-bs-target="#carousel${i}" data-bs-slide="next">
            <span class="carousel-control-next-icon"></span>
           </button>

           <div class="carousel-indicators">
            ${gr.graficos.map((_,index)=>`
             <button type="button" data-bs-target="#carousel${i}" data-bs-slide-to="${index}" ${index===0?'class="active"':''}></button>
            `).join('')}
           </div>

          </div>
         </div>
        </div>
       </div>
      </div>`;
   });
 }
}catch(e){console.log(e)}
});


async function carregarCarouselAnimais(){
 const container=document.getElementById('animaisCarouselInner');
 if(!container) return;
 try{
  const animais=await fetch('data/animais-destaque.json').then(r=>r.json());
  const cardsPorSlide=4;
  container.innerHTML='';
  for(let i=0;i<animais.length;i+=cardsPorSlide){
   const grupo=animais.slice(i,i+cardsPorSlide);
   container.innerHTML+=`<div class="carousel-item ${i===0?'active':''}"><div class="row g-4">
   ${grupo.map(animal=>`<div class="col-md-3"><div class="card animal-card h-100 shadow-sm border-0" onclick="abrirAnimalDestaque('${animal.especieBusca}')"><div class="animal-img-wrapper"><img src="${animal.imagem}" class="animal-img"></div><div class="card-body"><h5 class="fw-bold mb-1">${animal.nome}</h5><p class="text-muted mb-0 fst-italic">${animal.cientifico}</p></div></div></div>`).join('')}
   </div></div>`;
  }
 }catch(e){console.log(e)}
}

async function abrirAnimalDestaque(nomeEspecie){
 const modalCorpo=document.getElementById('detalheModalCorpo');
 const animais=await fetch('data/animais-destaque.json').then(r=>r.json()).catch(()=>[]);
 const animal=animais.find(a=>a.especieBusca===nomeEspecie);
 if(animal && animal.imagem){
   modalCorpo.innerHTML=`<div class="mb-4"><img src="${animal.imagem}" class="img-fluid rounded-4 w-100"></div>`;
 }
 await buscarFichaEspecie(nomeEspecie);
 if(animal && animal.imagem){
   modalCorpo.innerHTML=`<div class="mb-4"><img src="${animal.imagem}" class="img-fluid rounded-4 w-100"></div>`+modalCorpo.innerHTML;
 }
}

document.addEventListener('DOMContentLoaded',()=>setTimeout(carregarCarouselAnimais,500));
