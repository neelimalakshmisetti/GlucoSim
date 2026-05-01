/* ── GlucoSim app.js ── */

/* ── 1. PARTICLES ── */
(function(){
  const c=document.getElementById('particle-canvas');
  if(!c)return;
  const ctx=c.getContext('2d');
  let W,H,pts=[];
  function resize(){W=c.width=window.innerWidth;H=c.height=window.innerHeight}
  resize();window.addEventListener('resize',resize);
  function make(){return{x:Math.random()*W,y:Math.random()*H,r:Math.random()*1.8+0.4,dx:(Math.random()-0.5)*0.25,dy:(Math.random()-0.5)*0.25,o:Math.random()*0.5+0.2}}
  for(let i=0;i<90;i++)pts.push(make());
  function draw(){
    ctx.clearRect(0,0,W,H);
    pts.forEach(p=>{
      p.x+=p.dx;p.y+=p.dy;
      if(p.x<0)p.x=W;if(p.x>W)p.x=0;
      if(p.y<0)p.y=H;if(p.y>H)p.y=0;
      ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
      const g=ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,p.r*3);
      g.addColorStop(0,'rgba(167,139,250,'+p.o+')');
      g.addColorStop(1,'rgba(6,182,212,0)');
      ctx.fillStyle=g;ctx.fill();
    });
    // connections
    for(let i=0;i<pts.length;i++)for(let j=i+1;j<pts.length;j++){
      const dx=pts[i].x-pts[j].x,dy=pts[i].y-pts[j].y,d=Math.sqrt(dx*dx+dy*dy);
      if(d<120){ctx.strokeStyle='rgba(124,58,237,'+(0.08*(1-d/120))+')';ctx.lineWidth=0.5;ctx.beginPath();ctx.moveTo(pts[i].x,pts[i].y);ctx.lineTo(pts[j].x,pts[j].y);ctx.stroke();}
    }
    requestAnimationFrame(draw);
  }
  draw();
})();

/* ── 2. CURSOR ── */
(function(){
  const cur=document.getElementById('cursor'),ring=document.getElementById('cursor-ring');
  if(!cur)return;
  let mx=0,my=0,rx=0,ry=0;
  document.addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY;cur.style.left=mx+'px';cur.style.top=my+'px';});
  (function anim(){rx+=(mx-rx)*0.12;ry+=(my-ry)*0.12;ring.style.left=rx+'px';ring.style.top=ry+'px';requestAnimationFrame(anim);})();
  document.querySelectorAll('.btn,button,input,select,a,.food-option,.food-tag').forEach(el=>{
    el.addEventListener('mouseenter',()=>{ring.style.width='60px';ring.style.height='60px';ring.style.borderColor='rgba(124,58,237,0.8)';});
    el.addEventListener('mouseleave',()=>{ring.style.width='40px';ring.style.height='40px';ring.style.borderColor='rgba(6,182,212,0.5)';});
  });
})();

/* ── 3. MAGNETIC BUTTONS ── */
document.querySelectorAll('.btn').forEach(btn=>{
  btn.addEventListener('mousemove',e=>{
    const r=btn.getBoundingClientRect();
    const dx=e.clientX-r.left-r.width/2,dy=e.clientY-r.top-r.height/2;
    btn.style.transform=`translate(${dx*0.18}px,${dy*0.18}px)`;
  });
  btn.addEventListener('mouseleave',()=>{btn.style.transform='';});
  btn.addEventListener('click',e=>{
    const rip=document.createElement('span');rip.className='ripple';
    const r=btn.getBoundingClientRect(),s=Math.max(r.width,r.height);
    rip.style.cssText=`width:${s}px;height:${s}px;left:${e.clientX-r.left-s/2}px;top:${e.clientY-r.top-s/2}px`;
    btn.appendChild(rip);setTimeout(()=>rip.remove(),700);
  });
});

/* ── 4. CARD TILT ── */
function initTilt(){
  document.querySelectorAll('.tilt-card').forEach(card=>{
    card.addEventListener('mousemove',e=>{
      const r=card.getBoundingClientRect();
      const x=((e.clientX-r.left)/r.width-0.5)*14;
      const y=((e.clientY-r.top)/r.height-0.5)*-14;
      card.style.transform=`perspective(600px) rotateX(${y}deg) rotateY(${x}deg) scale(1.03)`;
    });
    card.addEventListener('mouseleave',()=>{card.style.transform='';});
  });
}

/* ── 5. COLLAPSIBLE ── */
document.getElementById('analysisToggle').addEventListener('click',function(){
  const body=document.getElementById('analysisBody');
  this.classList.toggle('open');body.classList.toggle('open');
});

/* ── 6. SLIDERS ── */
const actSlider=document.getElementById('activitySlider');
const actVal=document.getElementById('activityVal');
actSlider.addEventListener('input',()=>{
  const v=+actSlider.value;
  actVal.textContent=v<-15?'Sedentary':v<0?'Light':v===0?'Moderate':v<15?'Active':'Very Active';
});

const horSlider=document.getElementById('horizonSlider');
const horVal=document.getElementById('horizonVal');
horSlider.addEventListener('input',()=>{horVal.textContent=horSlider.value+' min';});

const medTimeSlider=document.getElementById('medTimeSlider');
const medTimeVal=document.getElementById('medTimeVal');
medTimeSlider.addEventListener('input',()=>{medTimeVal.textContent=medTimeSlider.value+' min ago';});

/* ── 7. MEDICATION TOGGLE ── */
const medToggle=document.getElementById('medToggle');
const medFields=document.getElementById('medFields');
const medDoseLabel=document.getElementById('medDoseLabel');
const medType=document.getElementById('medType');
medToggle.addEventListener('change',()=>{medFields.style.display=medToggle.checked?'block':'none';});
medType.addEventListener('change',()=>{
  medDoseLabel.textContent=medType.value==='Insulin'?'Dose (units)':'Dose (mg)';
  document.getElementById('medDose').value=medType.value==='Metformin'?500:medType.value==='Insulin'?5:100;
});

/* ── 8. FOOD DATA (embedded) ── */
let FOODS=[
  {food:"White rice (boiled)",carbs:40,fiber:1,fat:0.5,protein:4,gi:73,gl:29.2},
  {food:"Brown rice",carbs:38,fiber:2,fat:1.5,protein:4,gi:68,gl:25.8},
  {food:"Basmati rice",carbs:39,fiber:1,fat:0.5,protein:4,gi:58,gl:22.6},
  {food:"Chapati (whole wheat)",carbs:20,fiber:3,fat:1.5,protein:5,gi:62,gl:12.4},
  {food:"Paratha (plain)",carbs:25,fiber:2,fat:7,protein:4,gi:59,gl:14.8},
  {food:"Idli (2 pcs)",carbs:28,fiber:2,fat:1,protein:6,gi:60,gl:16.8},
  {food:"Dosa (plain)",carbs:30,fiber:2,fat:2,protein:4,gi:65,gl:19.5},
  {food:"Poha",carbs:35,fiber:3,fat:4,protein:5,gi:69,gl:24.2},
  {food:"Upma",carbs:32,fiber:3,fat:6,protein:6,gi:68,gl:21.8},
  {food:"Biryani",carbs:60,fiber:4,fat:12,protein:12,gi:70,gl:42},
  {food:"Khichdi",carbs:45,fiber:5,fat:6,protein:10,gi:55,gl:24.8},
  {food:"Dal (lentil curry)",carbs:30,fiber:6,fat:6,protein:12,gi:32,gl:9.6},
  {food:"Rajma curry",carbs:35,fiber:7,fat:7,protein:14,gi:28,gl:9.8},
  {food:"Chole (chickpea curry)",carbs:34,fiber:8,fat:8,protein:12,gi:36,gl:12.2},
  {food:"Sambar",carbs:18,fiber:4,fat:3,protein:7,gi:38,gl:6.8},
  {food:"Samosa (1 pc)",carbs:25,fiber:3,fat:12,protein:5,gi:48,gl:12},
  {food:"Pakora (bhajiya)",carbs:20,fiber:3,fat:10,protein:6,gi:46,gl:9.2},
  {food:"Pav Bhaji",carbs:50,fiber:6,fat:12,protein:8,gi:61,gl:30.5},
  {food:"Vada Pav",carbs:45,fiber:4,fat:10,protein:7,gi:60,gl:27},
  {food:"Gulab Jamun (2 pcs)",carbs:45,fiber:1,fat:12,protein:4,gi:76,gl:34.2},
  {food:"Rasgulla (2 pcs)",carbs:35,fiber:0,fat:5,protein:6,gi:63,gl:22},
  {food:"Jalebi (50g)",carbs:40,fiber:0,fat:5,protein:2,gi:82,gl:32.8},
  {food:"Laddoo (besan, 50g)",carbs:28,fiber:2,fat:8,protein:6,gi:60,gl:16.8},
  {food:"Kheer (rice pudding)",carbs:35,fiber:0,fat:8,protein:7,gi:65,gl:22.8},
  {food:"Chai (with sugar & milk)",carbs:12,fiber:0,fat:4,protein:4,gi:58,gl:7},
  {food:"Lassi (sweet)",carbs:28,fiber:0,fat:8,protein:9,gi:65,gl:18.2},
  {food:"Mango shake",carbs:45,fiber:2,fat:6,protein:6,gi:70,gl:31.5},
  {food:"Potato curry",carbs:35,fiber:4,fat:10,protein:5,gi:78,gl:27.3},
  {food:"Paneer curry",carbs:20,fiber:2,fat:15,protein:14,gi:34,gl:6.8},
  {food:"Bhindi (okra) curry",carbs:18,fiber:5,fat:8,protein:5,gi:35,gl:6.3},
  {food:"Aloo paratha",carbs:38,fiber:3,fat:8,protein:6,gi:77,gl:29.3},
  {food:"Masala dosa",carbs:40,fiber:3,fat:8,protein:6,gi:72,gl:28.8},
  {food:"Vegetable pulao",carbs:45,fiber:4,fat:10,protein:7,gi:70,gl:31.5},
  {food:"Pizza (veg, 1 slice)",carbs:30,fiber:2,fat:12,protein:10,gi:80,gl:24},
  {food:"Burger (veg)",carbs:45,fiber:3,fat:18,protein:14,gi:66,gl:29.7},
  {food:"French fries (medium)",carbs:40,fiber:3,fat:17,protein:4,gi:75,gl:30},
  {food:"Noodles (veg, Hakka)",carbs:50,fiber:4,fat:12,protein:8,gi:68,gl:34},
  {food:"Fried rice (veg)",carbs:48,fiber:3,fat:10,protein:8,gi:72,gl:34.6},
  {food:"Manchurian (veg balls)",carbs:36,fiber:4,fat:14,protein:10,gi:70,gl:25.2},
  {food:"Pongal (ven pongal)",carbs:42,fiber:3,fat:12,protein:8,gi:55,gl:23.1},
  {food:"Idiyappam (string hoppers)",carbs:40,fiber:2,fat:2,protein:5,gi:68,gl:27.2},
  {food:"Medu vada (2 pcs)",carbs:28,fiber:3,fat:10,protein:6,gi:64,gl:17.9},
  {food:"Appam with stew",carbs:44,fiber:3,fat:10,protein:6,gi:70,gl:30.8},
  {food:"Thepla (2 pcs)",carbs:28,fiber:4,fat:8,protein:6,gi:58,gl:16.2},
  {food:"Dhokla (100g)",carbs:20,fiber:2,fat:4,protein:6,gi:35,gl:7},
  {food:"Undhiyu",carbs:36,fiber:5,fat:14,protein:8,gi:55,gl:19.8},
  {food:"Misal pav",carbs:52,fiber:6,fat:14,protein:12,gi:68,gl:35.4},
  {food:"Chole bhature",carbs:60,fiber:6,fat:20,protein:14,gi:78,gl:46.8},
  {food:"Paneer butter masala",carbs:28,fiber:2,fat:18,protein:14,gi:55,gl:15.4},
  {food:"Halwa (Sooji)",carbs:45,fiber:1,fat:12,protein:4,gi:75,gl:34},
  {food:"Chicken Curry",carbs:5,fiber:1,fat:15,protein:28,gi:0,gl:0},
  {food:"Butter Chicken",carbs:15,fiber:2,fat:20,protein:30,gi:35,gl:5},
  {food:"Chicken Biryani",carbs:65,fiber:3,fat:15,protein:20,gi:70,gl:46},
  {food:"Fish Curry",carbs:6,fiber:1,fat:12,protein:26,gi:0,gl:0},
  {food:"Egg Curry",carbs:7,fiber:1,fat:12,protein:18,gi:0,gl:0},
  {food:"Mutton Curry",carbs:10,fiber:1,fat:20,protein:25,gi:0,gl:0},
  {food:"Samosa",carbs:25,fiber:2,fat:12,protein:4,gi:75,gl:19},
  {food:"Kachori",carbs:28,fiber:2,fat:15,protein:5,gi:78,gl:22},
  {food:"Ice Cream",carbs:28,fiber:0,fat:11,protein:4,gi:60,gl:17},
  {food:"Chocolate Cake",carbs:50,fiber:2,fat:15,protein:5,gi:75,gl:38}
];
function loadFoods(){initFoodUI();}

/* ── 9. FOOD UI ── */
let selectedFoods=[];
function initFoodUI(){
  const search=document.getElementById('foodSearch');
  const dropdown=document.getElementById('foodDropdown');
  function renderDropdown(q){
    const filtered=FOODS.filter(f=>f.food.toLowerCase().includes(q.toLowerCase())&&!selectedFoods.find(s=>s.food===f.food));
    dropdown.innerHTML=filtered.slice(0,20).map(f=>`<div class="food-option" data-food="${f.food}">${f.food}</div>`).join('');
    dropdown.classList.toggle('open',filtered.length>0&&q.length>0);
  }
  search.addEventListener('input',()=>renderDropdown(search.value));
  search.addEventListener('focus',()=>{if(search.value)renderDropdown(search.value);});
  document.addEventListener('click',e=>{if(!e.target.closest('.food-search-wrap'))dropdown.classList.remove('open');});
  dropdown.addEventListener('click',e=>{
    const opt=e.target.closest('.food-option');
    if(!opt)return;
    const name=opt.dataset.food;
    const food=FOODS.find(f=>f.food===name);
    if(food){selectedFoods.push({...food,servings:1});renderSelectedFoods();search.value='';dropdown.classList.remove('open');}
  });
}
function renderSelectedFoods(){
  const tagsEl=document.getElementById('selectedFoods');
  const inputsEl=document.getElementById('servingInputs');
  tagsEl.innerHTML=selectedFoods.map((f,i)=>
    `<div class="food-tag">${f.food}<span class="remove" data-i="${i}">×</span></div>`).join('');
  inputsEl.innerHTML=selectedFoods.map((f,i)=>`
    <div class="serving-row">
      <span class="food-name">${f.food}</span>
      <label style="margin:0;font-size:0.75rem;color:var(--text-muted)">Servings</label>
      <input type="number" min="0.5" max="5" step="0.5" value="${f.servings}" data-i="${i}" style="width:80px;padding:6px 10px">
    </div>`).join('');
  tagsEl.querySelectorAll('.remove').forEach(el=>{
    el.addEventListener('click',()=>{selectedFoods.splice(+el.dataset.i,1);renderSelectedFoods();});
  });
  inputsEl.querySelectorAll('input').forEach(inp=>{
    inp.addEventListener('change',()=>{selectedFoods[+inp.dataset.i].servings=+inp.value||1;});
  });
}

/* ── 10. SIMULATION ── */
function getMedEffect(type,dose,timeSince,T){
  const eff=new Float64Array(T.length);
  const profiles={
    'Metformin':{peak:180,dur:720,scale:0.8},
    'Sulfonylureas':{peak:120,dur:480,scale:1.2},
    'DPP-4 Inhibitors':{peak:150,dur:600,scale:0.6},
    'SGLT2 Inhibitors':{peak:90,dur:720,scale:0.5},
    'Insulin':{peak:90,dur:240,scale:2.0}
  };
  const p=profiles[type];if(!p)return eff;
  for(let i=0;i<T.length;i++){
    const t=T[i]+timeSince;
    if(t<0||t>p.dur)continue;
    eff[i]=Math.exp(-0.5*Math.pow((t-p.peak)/(p.peak/2),2))*dose*p.scale;
  }
  return eff;
}

function simulate(foods,baseline,weight,actFactor,horizon,medType,medDose,medTime){
  const N=horizon+1,T=Float64Array.from({length:N},(_,i)=>i);
  const delta=new Float64Array(N);
  const sens=3.5*(70/Math.max(40,weight))*(1+actFactor);
  const kd=0.012;
  for(const f of foods){
    const s=f.servings,carbs=f.carbs*s,fiber=f.fiber*s,fat=f.fat*s,protein=f.protein*s;
    const avail=Math.max(carbs-0.5*fiber,0);
    let ka=0.015+0.0006*f.gi;ka/=(1+0.01*fat+0.003*protein);
    const app=T.map(t=>avail*ka*Math.exp(-ka*t));
    const resp=app.map(v=>sens*v);
    const kern=T.map(t=>Math.exp(-kd*t));
    // convolve
    for(let i=0;i<N;i++)for(let j=0;j<=i;j++)delta[i]+=resp[j]*kern[i-j];
  }
  const medEff=medType?getMedEffect(medType,medDose,medTime,T):new Float64Array(N);
  const glucoNoMed=Float64Array.from({length:N},(_,i)=>Math.max(baseline+delta[i],70));
  const glucoMed=Float64Array.from({length:N},(_,i)=>Math.max(baseline+delta[i]-medEff[i],70));
  return{T,glucoNoMed,glucoMed,delta,medEff};
}

/* ── 11. CHART ── */
let chartInst=null;
function renderChart(T,noMed,med,baseline){
  const labels=Array.from(T);
  const ctx=document.getElementById('glucoseChart').getContext('2d');
  if(chartInst)chartInst.destroy();
  chartInst=new Chart(ctx,{
    type:'line',
    data:{
      labels,
      datasets:[
        {label:'Without Medication',data:Array.from(noMed),borderColor:'rgba(103,232,249,0.9)',backgroundColor:'rgba(103,232,249,0.05)',borderWidth:2.5,pointRadius:0,tension:0.4,fill:true},
        {label:'With Medication',data:Array.from(med),borderColor:'rgba(167,139,250,0.9)',backgroundColor:'rgba(167,139,250,0.05)',borderWidth:2.5,pointRadius:0,tension:0.4,fill:true}
      ]
    },
    options:{
      responsive:true,animation:{duration:1000,easing:'easeInOutQuart'},
      interaction:{mode:'index',intersect:false},
      plugins:{
        legend:{display:false},
        tooltip:{backgroundColor:'rgba(10,10,46,0.9)',borderColor:'rgba(124,58,237,0.4)',borderWidth:1,titleColor:'#e2e8f0',bodyColor:'#94a3b8',padding:12},
        annotation:{annotations:{
          baseline:{type:'line',yMin:baseline,yMax:baseline,borderColor:'rgba(244,63,94,0.6)',borderWidth:1.5,borderDash:[6,4],label:{content:'Baseline',display:true,position:'end',backgroundColor:'rgba(244,63,94,0.15)',color:'#fda4af',font:{size:11}}},
          rangeBox:{type:'box',yMin:70,yMax:180,backgroundColor:'rgba(16,185,129,0.06)',borderColor:'rgba(16,185,129,0.15)',borderWidth:1}
        }}
      },
      scales:{
        x:{title:{display:true,text:'Time (minutes)',color:'#94a3b8'},ticks:{color:'#94a3b8',maxTicksLimit:12},grid:{color:'rgba(255,255,255,0.04)'}},
        y:{title:{display:true,text:'Glucose (mg/dL)',color:'#94a3b8'},min:60,max:320,ticks:{color:'#94a3b8'},grid:{color:'rgba(255,255,255,0.04)'}}
      }
    }
  });
}

/* ── 12. SIMULATE BUTTON ── */
document.getElementById('simulateBtn').addEventListener('click',()=>{
  if(!selectedFoods.length){alert('Please select at least one food item.');return;}
  const baseline=+document.getElementById('glucoseInput').value||120;
  const weight=+document.getElementById('weightInput').value||70;
  const actFactor=(+document.getElementById('activitySlider').value)/100;
  const horizon=+document.getElementById('horizonSlider').value||180;
  const useMed=document.getElementById('medToggle').checked;
  const medType=useMed?document.getElementById('medType').value:null;
  const medDose=useMed?+document.getElementById('medDose').value:0;
  const medTime=useMed?+document.getElementById('medTimeSlider').value:0;

  // show loading
  document.getElementById('loadingState').style.display='block';
  document.getElementById('resultsSection').style.display='none';

  setTimeout(()=>{
    const{T,glucoNoMed,glucoMed}=simulate(selectedFoods,baseline,weight,actFactor,horizon,medType,medDose,medTime);
    const gluco=glucoMed;

    // metrics
    let peakIdx=0;for(let i=1;i<gluco.length;i++)if(gluco[i]>gluco[peakIdx])peakIdx=i;
    const peakVal=gluco[peakIdx],peakTime=T[peakIdx];
    let rtIdx=null;for(let i=peakIdx;i<gluco.length;i++)if(gluco[i]<=baseline+5){rtIdx=i;break;}
    const tir=gluco.filter(v=>v>=70&&v<=180).length/gluco.length*100;

    document.getElementById('metPeak').textContent=peakVal.toFixed(0)+' mg/dL';
    document.getElementById('metPeakSub').textContent='+'+(peakVal-baseline).toFixed(0)+' from baseline';
    document.getElementById('metTimePeak').textContent=peakTime+' min';
    document.getElementById('metReturn').textContent=rtIdx?T[rtIdx]+' min':'> Horizon';
    document.getElementById('metReturnSub').textContent=rtIdx?'after meal':'not reached';
    document.getElementById('metTIR').textContent=tir.toFixed(0)+'%';

    // analysis panel
    const peakColor=peakVal>180?'#f43f5e':peakVal>140?'#f59e0b':'#10b981';
    document.getElementById('analysisPeak').style.color=peakColor;
    document.getElementById('analysisPeak').textContent=peakVal.toFixed(0)+' mg/dL';
    document.getElementById('analysisPeakTime').textContent='at '+peakTime+' minutes';
    document.getElementById('analysisBaseline').textContent=baseline;

    // status badge
    const badge=document.getElementById('glucoseStatusBadge');
    if(peakVal>180){badge.className='status-badge status-high';badge.textContent='⚠ High Glucose Predicted';}
    else if(peakVal>140){badge.className='status-badge status-warn';badge.textContent='↑ Slightly Elevated';}
    else{badge.className='status-badge status-ok';badge.textContent='✓ Within Target Range';}

    // recommendations
    const recBox=document.getElementById('recommendationBox');
    let recHtml='';
    if(peakVal>180)recHtml=`<div class="alert alert-danger"><strong>⚠ High Glucose Alert</strong><ul><li>Consider reducing carbohydrate intake</li><li>Review medication timing with your healthcare provider</li><li>Engage in light physical activity after meals</li></ul></div>`;
    else if(peakVal>140)recHtml=`<div class="alert alert-warning"><strong>↑ Slightly Elevated</strong><ul><li>Monitor your levels closely</li><li>Consider a short walk after meals</li><li>Stay hydrated and maintain regular meal times</li></ul></div>`;
    else recHtml=`<div class="alert alert-success"><strong>✓ On Target</strong><ul><li>Maintain your current eating and activity patterns</li><li>Continue monitoring your glucose levels</li><li>Keep up the good work!</li></ul></div>`;
    if(gluco.some(v=>v<70))recHtml+=`<div class="alert alert-danger"><strong>⚠ Low Glucose Warning</strong><ul><li>Consider reducing medication dose</li><li>Eat a small snack with protein and complex carbs</li><li>Always carry fast-acting glucose sources</li></ul></div>`;
    recBox.innerHTML=recHtml;

    // meal table
    const tbody=document.getElementById('mealTableBody');
    tbody.innerHTML=selectedFoods.map(f=>`<tr>
      <td>${f.food}</td><td>${f.servings}</td>
      <td>${(f.carbs*f.servings).toFixed(1)}</td><td>${(f.fiber*f.servings).toFixed(1)}</td>
      <td>${(f.fat*f.servings).toFixed(1)}</td><td>${(f.protein*f.servings).toFixed(1)}</td>
      <td>${f.gi}</td><td>${(f.gl*f.servings).toFixed(1)}</td>
    </tr>`).join('');

    // chart
    renderChart(T,glucoNoMed,glucoMed,baseline);

    document.getElementById('loadingState').style.display='none';
    document.getElementById('resultsSection').style.display='block';
    document.getElementById('resultsSection').scrollIntoView({behavior:'smooth',block:'start'});

    initTilt();
  },800);
});

/* ── 13. INIT ── */
loadFoods();
