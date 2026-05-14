
const TERRITORY_IMAGES={
alagoinhas:"/assets/territorios/alagoinhas.webp",salvador:"/assets/territorios/salvador.webp",
feira:"/assets/territorios/feira.webp",reconcavo:"/assets/territorios/reconcavo.webp",
chapada:"/assets/territorios/chapada.webp",oeste:"/assets/territorios/oeste.webp",
norte:"/assets/territorios/norte.webp",sul:"/assets/territorios/sul.webp"
};
function applyTerritoryMirror(slug,label){
 const page=document.querySelector(".trindade-page"), hero=document.querySelector(".hero-copy");
 if(!page||!TERRITORY_IMAGES[slug]) return;
 page.style.setProperty("--territory-bg",`url('${TERRITORY_IMAGES[slug]}')`);
 if(hero&&!document.querySelector(".territory-signature")){
   const b=document.createElement("div");b.className="territory-signature";b.textContent=label||"Bahia em movimento";hero.appendChild(b);
 }
}
applyTerritoryMirror("alagoinhas","Base territorial: Alagoinhas e Litoral Norte");
