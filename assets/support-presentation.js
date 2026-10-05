
'use strict';
const slides=[...document.querySelectorAll('.slide')];
const prev=document.querySelector('#prev'),next=document.querySelector('#next'),counter=document.querySelector('#counter'),progress=document.querySelector('#progress');
const dialog=document.querySelector('#image-dialog'),largeImage=document.querySelector('#large-image');
const status=document.querySelector('#status');
let current=0,statusTimeout;
function announce(text){status.textContent=text;clearTimeout(statusTimeout);statusTimeout=setTimeout(()=>status.textContent='',6000)}
function fromHash(){const match=location.hash.match(/^#slide-(\d+)$/);return match?Number(match[1])-1:0}
function show(index){current=Math.max(0,Math.min(slides.length-1,Number.isFinite(index)?index:0));slides.forEach((slide,i)=>slide.hidden=i!==current);counter.textContent=`${current+1} / ${slides.length}`;prev.disabled=current===0;next.disabled=current===slides.length-1;progress.style.width=`${(current+1)/slides.length*100}%`;history.replaceState(null,'',`#slide-${current+1}`);window.scrollTo(0,0)}
prev.addEventListener('click',()=>show(current-1));next.addEventListener('click',()=>show(current+1));
window.addEventListener('hashchange',()=>show(fromHash()));
const full=document.querySelector('#full');
full.addEventListener('click',async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else if(document.documentElement.requestFullscreen)await document.documentElement.requestFullscreen();else announce('Разверните окно браузера для удобного просмотра.')}catch{announce('Разверните окно браузера для удобного просмотра.')}});
document.addEventListener('fullscreenchange',()=>{full.setAttribute('aria-label',document.fullscreenElement?'Выйти из полного экрана':'На полный экран');full.textContent=document.fullscreenElement?'⛶ Выйти':'⛶ Экран'});
document.addEventListener('keydown',e=>{
 if(dialog.open||e.altKey||e.ctrlKey||e.metaKey||e.shiftKey||e.target.closest('input,textarea,select,[contenteditable="true"]'))return;
 if(e.target.closest('a,button')&&[' ','Enter'].includes(e.key))return;
 if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();show(current+1)}
 else if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();show(current-1)}
 else if(e.key==='Home'){e.preventDefault();show(0)}
 else if(e.key==='End'){e.preventDefault();show(slides.length-1)}
 else if(e.key.toLowerCase()==='f'){e.preventDefault();full.click()}
});
let start=null;
document.querySelector('.deck').addEventListener('touchstart',e=>{if(e.target.closest('a,button'))return;start={x:e.touches[0].clientX,y:e.touches[0].clientY}},{passive:true});
document.querySelector('.deck').addEventListener('touchend',e=>{if(!start)return;const dx=e.changedTouches[0].clientX-start.x,dy=e.changedTouches[0].clientY-start.y;if(Math.abs(dx)>70&&Math.abs(dx)>Math.abs(dy)*1.4)show(current+(dx<0?1:-1));start=null},{passive:true});
for(const button of document.querySelectorAll('.zoom-shot'))button.addEventListener('click',()=>{const img=button.querySelector('img');largeImage.src=img.src;largeImage.alt=img.alt;dialog.showModal()});
document.querySelector('#close-image').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close()}});
document.querySelector('#share').addEventListener('click',async()=>{const url='https://jobhub.today/support-presentation';try{await navigator.clipboard.writeText(url);announce('Ссылка на презентацию скопирована. Можно отправить её работодателю.')}catch{announce('Скопируйте ссылку из адресной строки браузера.')}});
show(fromHash());
