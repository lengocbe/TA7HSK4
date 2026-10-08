'use strict';
const $ = s => document.querySelector(s);
const ICONS = {
 book:'<path d="M12 7c-3-3-7-3-10-2v14c3-1 7-1 10 2 3-3 7-3 10-2V5c-3-1-7-1-10 2zm0 0v14"/>',
 home:'<path d="m3 10 9-7 9 7v11h-6v-7H9v7H3z"/>',
 layers:'<path d="m12 3 10 6-10 6L2 9zM2 14l10 6 10-6M2 19l10 6 10-6"/>',
 chart:'<path d="M4 20V10m8 10V4m8 16v-7M2 22h20"/>',
 settings:'<path d="M4 6h16M4 12h16M4 18h16"/><circle cx="8" cy="6" r="2"/><circle cx="16" cy="12" r="2"/><circle cx="10" cy="18" r="2"/>',
 sound:'<path d="m3 9 4 0 5-4v14l-5-4H3zM16 8c3 2 3 6 0 8M19 5c5 4 5 10 0 14"/>',
 arrow:'<path d="M5 12h14m-5-5 5 5-5 5"/>',
 back:'<path d="m15 5-7 7 7 7"/>',
 chevron:'<path d="m9 5 7 7-7 7"/>',
 check:'<path d="m5 12 4 4L19 6"/>',
 offline:'<path d="m3 4 18 17M2 9a17 17 0 0 1 5-3m3-1a17 17 0 0 1 12 4M5 13a12 12 0 0 1 5-2m4 0a12 12 0 0 1 5 2M8 17a6 6 0 0 1 8 0"/><circle cx="12" cy="21" r="1"/>',
 search:'<circle cx="10" cy="10" r="7"/><path d="m15 15 6 6"/>',
 star:'<path d="m12 3 3 6 7 1-5 5 1 7-6-3-6 3 1-7-5-5 7-1z"/>',
 close:'<path d="m5 5 14 14M5 19 19 5"/>',
 trophy:'<path d="M7 3h10v7a5 5 0 0 1-10 0zM7 5H3v3c0 3 2 4 5 4m9-7h4v3c0 3-2 4-5 4M12 15v5M7 21h10"/>',
 clock:'<circle cx="12" cy="12" r="9"/><path d="M12 6v6l4 2"/>',
 download:'<path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5"/>',
 upload:'<path d="M12 16V4m-5 5 5-5 5 5M4 16v5h16v-5"/>',
 moon:'<path d="M20 15A9 9 0 0 1 9 4a9 9 0 1 0 11 11z"/>',
 flame:'<path d="M12 3c1 5 7 6 7 12a7 7 0 0 1-14 0c0-3 2-5 4-7 0 3 2 4 3 4 2-3 1-6 0-9z"/>'
};
function icon(name, cls=''){return `<svg class="icon ${cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[name]||ICONS.book}</svg>`;}
function esc(value){return String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
const LESSONS = DATA.lessons;
const WORDS = DATA.words;
const BYID = WORDS.reduce((map,w)=>{map[w.id]=w;return map;},Object.create(null));
const defaults = () => ({schema:1,progress:{},favorites:[],last:{},daily:{},settings:{dark:false,slow:false,goal:15}});
let state = defaults(), page='home', lang='en', lessonId=null, currentWord=null, section='units', study=null, search='', wordFilter='all', lastDetail='lesson', saveError=false;
let browserAudio=null;
function readState(){try{const raw=window.Android?Android.load():localStorage.getItem('lingo-state');if(raw) state=validateState(JSON.parse(raw));}catch(e){state=defaults();toast('Không đọc được tiến độ cũ. Hãy khôi phục bản sao lưu nếu có.');}}
function validateState(input){
 if(!input || input.schema!==1 || typeof input.progress!=='object'||Array.isArray(input.progress)||!input.progress) throw Error('Invalid backup');
 const out=defaults();
 for(const [id,p] of Object.entries(input.progress)){
  if(!BYID[id])continue;
  if(!p || !Number.isFinite(p.due)||!Number.isFinite(p.interval)||p.interval<0||p.interval>365||!Number.isInteger(p.reps)||p.reps<0||!Number.isInteger(p.lapses)||p.lapses<0) throw Error('Invalid progress');
  out.progress[id]={due:p.due,interval:p.interval,reps:p.reps,lapses:p.lapses,last:typeof p.last==='string'?p.last:''};
 }
 out.favorites=Array.isArray(input.favorites)?[...new Set(input.favorites.filter(id=>BYID[id]))]:[];
 for(const l of ['en','zh'])if(input.last?.[l] && LESSONS.some(x=>x.id===input.last[l]&&x.lang===l))out.last[l]=input.last[l];
 if(input.daily && typeof input.daily==='object')for(const [key,value]of Object.entries(input.daily))if(/^\d{4}-\d{2}-\d{2}$/.test(key)&&Number.isInteger(value)&&value>=0&&value<100000)out.daily[key]=value;
 out.settings={dark:!!input.settings?.dark,slow:!!input.settings?.slow,goal:[5,10,15,20,30].includes(input.settings?.goal)?input.settings.goal:15};
 return out;
}
function save(){try{if(window.Android){if(!Android.save(JSON.stringify(state)))throw Error('Save failed');}else localStorage.setItem('lingo-state',JSON.stringify(state));saveError=false;}catch(e){if(!saveError)toast('Không lưu được tiến độ. Hãy xuất bản sao lưu.');saveError=true;}}
function localDay(date=new Date()){return `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;}
function todayCount(){return state.daily[localDay()]||0;}
function languageName(l){return l==='en'?'Tiếng Anh':'Tiếng Hoa';}
function lessonWords(id){const lesson=LESSONS.find(l=>l.id===id);return lesson?lesson.words.map(id=>BYID[id]).filter(Boolean):[];}
function learned(words){return words.filter(w=>(state.progress[w.id]?.reps||0)>0).length;}
function dueWords(l){return WORDS.filter(w=>(!l||w.lang===l)&&state.progress[w.id]&&state.progress[w.id].due<=Date.now());}
function streak(){let n=0,d=new Date();if(!state.daily[localDay(d)])d.setDate(d.getDate()-1);while(state.daily[localDay(d)]){n++;d.setDate(d.getDate()-1);}return n;}
function percentage(n,total){return total?Math.round(n*100/total):0;}
function toast(message){const el=$('#toast');el.textContent=message;el.classList.add('show');clearTimeout(toast.timer);toast.timer=setTimeout(()=>el.classList.remove('show'),3500);}
function stopAudio(){if(window.Android)Android.stop();if(browserAudio){browserAudio.pause();browserAudio=null;}}
function playWord(id){
 if(!BYID[id])return;
 if(window.Android){Android.play(id,state.settings.slow);return;}
 stopAudio();browserAudio=new Audio(`audio/${id}.mp3`);browserAudio.playbackRate=state.settings.slow?.78:1;
 browserAudio.play().catch(()=>toast('Chưa phát được âm thanh. Hãy thử lại.'));
}
window.audioFailed=()=>toast('Không phát được âm thanh. Hãy thử lại.');
function applyTheme(){document.body.classList.toggle('dark',state.settings.dark);if(window.Android)Android.theme(state.settings.dark);}
function nav(){return `<nav class="nav" aria-label="Điều hướng">${[['home','home','Trang chủ'],['library','book','Bài học'],['words','layers','Kho từ'],['stats','chart','Tiến độ'],['settings','settings','Cài đặt']].map(([p,i,t])=>`<button data-action="nav" data-page="${p}" class="${page===p||(p==='library'&&page==='lesson')?'selected':''}">${icon(i)}<span>${t}</span></button>`).join('')}</nav>`;}
function audioButton(id){return `<button class="iconbtn audio" data-action="audio" data-id="${id}" aria-label="Nghe phát âm">${icon('sound')}</button>`;}
function languagePills(){return `<div class="pillbar"><button class="pill ${lang==='en'?'active':''}" data-action="lang" data-lang="en">Tiếng Anh</button><button class="pill ${lang==='zh'?'active':''}" data-action="lang" data-lang="zh">Tiếng Hoa</button></div>`;}
function backButton(text='Quay lại'){return `<button class="back" data-action="back">${icon('back')}${text}</button>`;}
function home(){
 const count=todayCount(),goal=state.settings.goal;
 return `<div class="topbar"><div class="brand"><b>lingo</b><small>SỔ TỪ VỰNG CỦA BẠN</small></div><button class="iconbtn avatar" data-action="nav" data-page="stats" aria-label="Xem chuỗi ngày học">${icon('flame')}</button></div>
 <div class="welcome"><div class="eyebrow">Mỗi ngày một bước tiến</div><h1 style="margin-top:8px">Hôm nay, học gì nhỉ?</h1><p>Chọn ngôn ngữ và bắt đầu hành trình của bạn.</p></div>
 <div class="card goal-card"><div class="goal-ring" style="--pct:${Math.min(100,count/goal*100)}%"><span>${Math.min(count,goal)}/${goal}</span></div><div><h3>${count>=goal?'Bạn đã đạt mục tiêu hôm nay!':'Một chút mỗi ngày, nhớ lâu hơn'}</h3><p>${count} lượt ôn hôm nay · Mục tiêu ${goal} lượt</p><button class="link-button" data-action="nav" data-page="settings">Điều chỉnh mục tiêu ${icon('chevron','chevron')}</button></div></div>
 <div class="section-head"><h2>Chọn ngôn ngữ</h2><span>2 hành trình</span></div><div class="stack languages">${['en','zh'].map(l=>{
 const words=WORDS.filter(w=>w.lang===l),done=learned(words),lesson=LESSONS.find(x=>x.id===state.last[l]);
 return `<button class="language-card ${l}" data-action="open-language" data-lang="${l}"><div class="lang-top"><div class="language-symbol">${l==='en'?'Aa':'汉'}</div><div><h2>${languageName(l)}</h2><p>${l==='en'?'Global Success · Lớp 7':'HSK 4 · Chữ giản thể'}</p></div></div><span class="badge">${LESSONS.filter(x=>x.lang===l&&x.kind==='unit').length} ${l==='en'?'Unit':'bài'} · ${words.length} từ vựng</span><div class="progress"><i style="width:${percentage(done,words.length)}%"></i></div><div class="row between small muted"><span>${done} từ đã học</span><span>${percentage(done,words.length)}%</span></div><div class="continue"><span>${lesson?'Học tiếp · '+esc(lesson.short):'Khám phá bài học'}</span>${icon('arrow')}</div></button>`;
 }).join('')}</div>${dueWords().length?`<div class="review-banner"><div><b>${dueWords().length} từ đến hạn ôn</b><span>Củng cố những từ bạn đã học</span></div><button data-action="review" data-lang="all">Ôn ngay</button></div>`:''}<div class="offline-note">${icon('offline')}Từ vựng và giọng đọc có sẵn · Học ngoại tuyến</div>`;
}
function lessonTile(l){const words=lessonWords(l.id),n=learned(words);return `<button class="lesson" data-action="lesson" data-id="${l.id}"><div class="lesson-icon">${esc(l.symbol||l.number||'↻')}</div><div class="lesson-main"><div class="eyebrow">${esc(l.short)}</div><h3>${esc(l.title)}</h3><p>${words.length} từ · ${n} đã học${dueWords(l.lang).filter(w=>l.words.includes(w.id)).length?' · Có từ cần ôn':''}</p><div class="progress"><i style="width:${percentage(n,words.length)}%"></i></div></div>${icon('chevron','chevron')}</button>`;}
function library(){
 const filtered=LESSONS.filter(l=>l.lang===lang&&l.kind===({units:'unit',review:'review',tests:'test'}[section]||'unit'));
 return `<div class="page-head">${backButton('Trang chủ')}<h1>${languageName(lang)}</h1><p>${lang==='en'?'Từ vựng theo sách Global Success lớp 7':'Bài học biên soạn từ 13 đề HSK 4'}</p></div>${languagePills()}<div class="pillbar"><button class="pill ${section==='units'?'active':''}" data-action="section" data-section="units">${lang==='en'?'12 Unit':'Theo chủ đề'}</button><button class="pill ${section===(lang==='en'?'review':'tests')?'active':''}" data-action="section" data-section="${lang==='en'?'review':'tests'}">${lang==='en'?'Ôn tập Review':'Theo đề HSK'}</button></div><div class="stack">${filtered.map(lessonTile).join('')}</div>`;
}
function wordRow(w){const p=state.progress[w.id];return `<div class="word-row"><span class="word-status ${p?.reps?'learned':''}" title="${p?.reps?'Đã học':'Chưa học'}"></span><button class="word-info" data-action="word" data-id="${w.id}"><b>${esc(w.text)}</b><span>${esc(w.pron)} · ${esc(w.meaning)}</span></button>${audioButton(w.id)}</div>`;}
function lessonPage(){const l=LESSONS.find(x=>x.id===lessonId);if(!l)return library();const words=lessonWords(l.id),newCount=words.filter(w=>!state.progress[w.id]?.reps).length,reviewCount=words.filter(w=>state.progress[w.id]?.due<=Date.now()).length;
 return `<div class="page-head">${backButton('Danh sách bài')}<div class="card hero-lesson" style="margin-top:13px"><div class="eyebrow">${esc(l.short)}</div><h2>${esc(l.title)}</h2><p>${esc(l.description)}</p><div class="progress"><i style="width:${percentage(learned(words),words.length)}%"></i></div><p>${learned(words)}/${words.length} từ đã học · ${reviewCount} đến hạn ôn</p></div></div>
 <div class="actions"><button class="primary" data-action="learn" data-mode="new">${icon('book')} ${newCount?`Học từ mới · ${newCount} từ`:'Học lại toàn bộ bài'}</button><div class="two"><button class="secondary" data-action="learn" data-mode="due">${icon('clock')}Ôn đến hạn (${reviewCount})</button><button class="secondary" data-action="quiz-menu">${icon('layers')}Luyện tập</button></div></div><div class="section-head"><h2>Từ vựng trong bài</h2><span>${words.length} từ</span></div><div class="card list-panel">${words.map(wordRow).join('')}</div><p class="source">${esc(l.source)}</p>`;
}
function wordsPage(){let words=WORDS.filter(w=>w.lang===lang);const q=search.trim().toLocaleLowerCase('vi').normalize('NFD').replace(/[\u0300-\u036f]/g,'');
 if(q)words=words.filter(w=>[w.text,w.meaning,w.pron].join(' ').toLocaleLowerCase('vi').normalize('NFD').replace(/[\u0300-\u036f]/g,'').includes(q));
 if(wordFilter==='saved')words=words.filter(w=>state.favorites.includes(w.id));if(wordFilter==='new')words=words.filter(w=>!state.progress[w.id]?.reps);if(wordFilter==='due')words=words.filter(w=>state.progress[w.id]?.due<=Date.now());
 return `<div class="page-head"><div class="eyebrow">Từ điển nhỏ của bạn</div><h1>Kho từ vựng</h1><p>Tìm từ, nghe phát âm và lưu những từ cần nhớ.</p></div>${languagePills()}<label class="search">${icon('search')}<input id="search" value="${esc(search)}" placeholder="Tìm từ, nghĩa hoặc pinyin…" aria-label="Tìm từ vựng" autocomplete="off"></label><div class="pillbar">${[['all','Tất cả'],['saved','Đã lưu'],['new','Chưa học'],['due','Cần ôn']].map(([v,t])=>`<button class="pill ${wordFilter===v?'active':''}" data-action="filter" data-filter="${v}">${t}</button>`).join('')}</div><p class="filter-count">${words.length} từ phù hợp</p><div class="card list-panel" id="word-results">${words.length?words.map(wordRow).join(''):'<div class="empty">Chưa có từ phù hợp.</div>'}</div>`;
}
function detailPage(){const w=BYID[currentWord];return `${backButton(lastDetail==='words'?'Kho từ vựng':'Từ vựng trong bài')}<div class="word-detail">${wordCard(w,true,true)}</div><button class="secondary" data-action="review-word" data-id="${w.id}">${icon('book')}Ôn từ này</button>`;}
function wordCard(w,reveal,detail=false){return `<div class="card study-card">${detail?`<button class="favorite ${state.favorites.includes(w.id)?'saved':''}" data-action="favorite" data-id="${w.id}" aria-label="${state.favorites.includes(w.id)?'Bỏ lưu từ':'Lưu từ'}">${icon('star')}</button>`:''}<div class="eyebrow">${w.lang==='en'?'English vocabulary':'汉语词汇'}</div><div class="word">${esc(w.text)}</div>${w.lang==='en'||reveal?`<div class="pronunciation">${esc(w.pron)}</div>`:'<div class="pronunciation">Đoán cách đọc và nghĩa</div>'}${audioButton(w.id)}${reveal?`<div class="meaning">${esc(w.meaning)}</div><div class="type-tag">${esc(w.pos)}</div>${w.example?`<div class="example"><b>${esc(w.example)}</b>${w.examplePron?`<p class="small muted">${esc(w.examplePron)}</p>`:''}<p class="translation">${esc(w.translation)}</p></div>`:''}<p class="source">${esc(w.source)}</p>`:''}</div>`;}
function shuffle(array){const out=[...array];for(let i=out.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[out[i],out[j]]=[out[j],out[i]];}return out;}
function startStudy(words,mode='cards',label='Ôn tập',context='lesson'){
 if(!words.length){toast('Chưa có từ đến hạn ôn trong mục này.');return;}
 stopAudio();study={queue:mode==='cards'?[...words]:shuffle(words),index:0,reveal:false,mode,label,context,correct:0,answered:false,choice:null,options:null};page='study';render();
}
function quizMenu(){const l=LESSONS.find(x=>x.id===lessonId);return `<div class="page-head">${backButton('Về bài học')}<h1>Luyện tập</h1><p>${esc(l.title)} · Chọn cách bạn muốn luyện</p></div><div class="stack">${[['meaning','Chọn nghĩa đúng','Nhìn từ và chọn nghĩa tiếng Việt.','book'],['reverse','Nhớ từ qua nghĩa','Chọn từ phù hợp với nghĩa cho trước.','layers'],['listening','Nghe và nhận diện','Nghe phát âm rồi chọn từ đúng.','sound'],['typing',lang==='en'?'Luyện chính tả':'Nhập chữ Hán','Nhìn nghĩa và nhập từ bằng bàn phím.','settings']].map(([mode,title,desc,i])=>`<button class="lesson" data-action="start-quiz" data-mode="${mode}"><div class="lesson-icon">${icon(i)}</div><div class="lesson-main"><h3>${title}</h3><p>${desc}</p></div>${icon('chevron','chevron')}</button>`).join('')}</div>`;}
function makeOptions(w){const pool=shuffle(WORDS.filter(x=>x.lang===w.lang&&x.id!==w.id&&x.meaning!==w.meaning));return shuffle([w,...pool.slice(0,3)]);}
function studyPage(){
 if(study.index>=study.queue.length)return donePage();
 const w=study.queue[study.index];lang=w.lang;
 const header=`<div class="study-top"><button class="iconbtn" data-action="exit-study" aria-label="Thoát lượt học">${icon('close')}</button><span>${esc(study.label)}</span><b class="small">${study.index+1}/${study.queue.length}</b></div><div class="progress"><i style="width:${percentage(study.index,study.queue.length)}%"></i></div>`;
 if(study.mode==='cards')return `${header}${wordCard(w,study.reveal)}<button class="speed-toggle ${state.settings.slow?'active':''}" data-action="slow">${icon('sound')}Giọng đọc ${state.settings.slow?'chậm':'bình thường'} · Bấm để đổi</button>${study.reveal?`<p class="hint">Bạn nhớ từ này ở mức nào?</p><div class="ratings">${[['again','Quên','10 phút'],['hard','Khó','1 ngày'],['good','Nhớ','Giãn lịch ôn'],['easy','Dễ','Ôn xa hơn']].map(([v,t,d])=>`<button class="rating" data-action="rate" data-rating="${v}">${t}<small>${d}</small></button>`).join('')}</div>`:`<p class="hint">Thử nhớ nghĩa trước khi mở thẻ nhé.</p><button class="primary" data-action="reveal">Hiện nghĩa ${icon('arrow')}</button>`}`;
 const mode=study.mode;
 if(!study.options)study.options=makeOptions(w);
 const prompt=mode==='meaning'?w.text:mode==='listening'?'Nghe và chọn từ đúng':w.meaning;
 const question=`<div class="card study-card" style="min-height:210px"><div class="eyebrow">${mode==='typing'?'Nhập từ phù hợp':'Chọn một đáp án'}</div><div class="word" style="font-size:${mode==='meaning'&&lang==='zh'?42:27}px">${esc(prompt)}</div>${mode==='listening'?audioButton(w.id):''}</div>`;
 const answer=mode==='typing'?`<input class="answer-input" id="typed-answer" aria-label="Nhập từ trả lời" placeholder="${lang==='en'?'Nhập từ tiếng Anh…':'Nhập chữ Hán giản thể…'}" autocapitalize="off" autocomplete="off" spellcheck="false" ${study.answered?'disabled':''}><button class="primary" data-action="check-typing" ${study.answered?'disabled':''}>Kiểm tra</button>`:study.options.map(o=>`<button class="choice ${study.answered?(o.id===w.id?'correct':o.id===study.choice?'wrong':''):''}" data-action="answer" data-id="${o.id}" ${study.answered?'disabled':''}>${esc(mode==='meaning'?o.meaning:o.text)}</button>`).join('');
 return `${header}${question}${answer}${study.answered?`<div class="feedback"><b>${study.choice===w.id?'Chính xác!':'Mình cùng ghi nhớ lại nhé.'}</b><p style="margin-top:8px">${esc(w.text)} · ${esc(w.pron)}<br>${esc(w.meaning)}</p><div style="margin-top:10px">${audioButton(w.id)}</div></div><button class="primary" data-action="next-question">${study.index===study.queue.length-1?'Xem kết quả':'Câu tiếp theo'} ${icon('arrow')}</button>`:''}`;
}
function markRated(id,rating){
 const p=state.progress[id]||{interval:0,reps:0,lapses:0};let interval;
 if(rating==='again')interval=10/1440;else if(rating==='hard')interval=1;else if(rating==='good')interval=p.reps?Math.max(2,Math.ceil(p.interval*2)):2;else interval=p.reps?Math.max(4,Math.ceil(p.interval*3)):4;
 interval=Math.min(365,interval);
 state.progress[id]={interval,due:Date.now()+interval*86400000,reps:p.reps+1,lapses:p.lapses+(rating==='again'?1:0),last:localDay()};
 state.daily[localDay()]=(state.daily[localDay()]||0)+1;save();
}
function donePage(){return `<div class="done"><div class="big-symbol">${icon('trophy')}</div><div class="eyebrow">Một bước tiến mới</div><h1 style="margin-top:10px">Bạn làm tốt lắm!</h1><p>${study.mode==='cards'?`Đã ôn ${study.queue.length} từ. App đã lưu tiến độ và lên lịch ôn tiếp.`:`Bạn trả lời đúng ${study.correct}/${study.queue.length} câu. Các từ đã được cập nhật lịch ôn.`}</p></div><div class="stats-grid"><div class="card stat"><strong>${study.queue.length}</strong><span>${study.mode==='cards'?'Từ vừa ôn':'Câu luyện tập'}</span></div><div class="card stat"><strong>${streak()}</strong><span>Ngày học liên tiếp</span></div></div><button class="primary" data-action="exit-study">Về bài học ${icon('arrow')}</button>`;}
function statsPage(){const words=WORDS.filter(w=>w.lang===lang),n=learned(words),due=dueWords(lang).length;const days=[];for(let i=6;i>=0;i--){const d=new Date();d.setDate(d.getDate()-i);days.push({label:d.getDate()+'/'+(d.getMonth()+1),value:state.daily[localDay(d)]||0});}const max=Math.max(...days.map(x=>x.value),state.settings.goal);
 return `<div class="page-head"><div class="eyebrow">Tích lũy từng ngày</div><h1>Tiến độ của bạn</h1><p>${streak()} ngày học liên tiếp · ${todayCount()} lượt ôn hôm nay</p></div>${languagePills()}<div class="stats-grid">${[[n,'Từ đã học','book'],[due,'Từ đến hạn ôn','clock'],[words.length-n,'Từ chưa học','layers'],[percentage(n,words.length)+'%','Tiến độ học từ','chart']].map(([v,t,i])=>`<div class="card stat">${icon(i)}<strong>${v}</strong><span>${t}</span></div>`).join('')}</div><div class="card"><h3>7 ngày gần đây</h3><p class="small muted">Lượt ôn của cả hai ngôn ngữ</p><div class="daily-bars">${days.map(x=>`<div class="day-bar"><b>${x.value}</b><i style="height:${Math.max(4,x.value/max*65)}px"></i><span>${x.label}</span></div>`).join('')}</div></div>${due?`<button class="primary" style="margin-top:18px" data-action="review" data-lang="${lang}">Ôn ${due} từ đến hạn ${icon('arrow')}</button>`:''}<div class="section-head"><h2>Theo bài học</h2></div><div class="stack">${LESSONS.filter(l=>l.lang===lang&&l.kind==='unit').map(lessonTile).join('')}</div>`;
}
function settingsPage(){return `<div class="page-head"><div class="eyebrow">Theo cách của bạn</div><h1>Cài đặt</h1><p>Một không gian học thoải mái và riêng tư.</p></div><div class="card"><div class="setting-row"><div><b>Giao diện tối</b><p>Dịu mắt khi học buổi tối</p></div><button class="toggle ${state.settings.dark?'on':''}" data-action="dark" aria-label="Giao diện tối" aria-pressed="${state.settings.dark}"><span></span></button></div><div class="setting-row"><div><b>Đọc chậm</b><p>Giảm tốc độ, giữ nguyên cao độ giọng</p></div><button class="toggle ${state.settings.slow?'on':''}" data-action="slow" aria-label="Đọc chậm" aria-pressed="${state.settings.slow}"><span></span></button></div><div class="setting-row"><div><b>Mục tiêu mỗi ngày</b><p>Số lượt ôn từ vựng</p></div><select id="daily-goal" aria-label="Mục tiêu mỗi ngày">${[5,10,15,20,30].map(n=>`<option value="${n}" ${state.settings.goal===n?'selected':''}>${n} lượt</option>`).join('')}</select></div></div><div class="section-head"><h2>Sao lưu tiến độ</h2></div><div class="stack"><button class="secondary" data-action="export">${icon('download')}Xuất bản sao lưu</button><button class="secondary" data-action="import">${icon('upload')}Khôi phục từ bản sao lưu</button></div><div class="notice">Bản sao lưu gồm tiến độ, từ đã lưu và cài đặt. Khôi phục sẽ thay thế tiến độ hiện tại sau khi bạn xác nhận. Nên sao lưu trước khi đổi điện thoại hoặc gỡ app.</div><div class="section-head"><h2>Về Lingo</h2><span>Phiên bản 1.0.0</span></div><div class="card stack"><div><b>Tiếng Anh</b><p class="small muted">Từ trọng tâm theo Glossary của sách Tiếng Anh 7 Global Success. Câu ví dụ trong app được biên soạn bổ sung.</p></div><div><b>Tiếng Hoa</b><p class="small muted">Chữ giản thể, pinyin và nghĩa tiếng Việt. Từ và câu nguồn được đối chiếu với 13 PDF đề HSK 4 đã cung cấp; đây không phải danh sách đầy đủ mọi từ HSK 4.</p></div><div><b>Giọng đọc ngoại tuyến</b><p class="small muted">Âm thanh tổng hợp cho từng từ được đóng gói sẵn. Không cần tải giọng đọc, không cần tài khoản hay kết nối mạng. Câu ví dụ hiện hiển thị bằng chữ.</p></div></div>`;}
function render(){applyTheme();let body;switch(page){case'home':body=home();break;case'library':body=library();break;case'lesson':body=lessonPage();break;case'words':body=wordsPage();break;case'detail':body=detailPage();break;case'quiz-menu':body=quizMenu();break;case'study':body=studyPage();break;case'stats':body=statsPage();break;case'settings':body=settingsPage();break;default:page='home';body=home();}
 $('#app').innerHTML=`<main class="screen ${page==='home'?'home-screen':''} ${lang==='zh'&&page!=='home'?'zh-tone':''} ${page==='study'?'study-screen':''}">${body}</main>${['study','detail','quiz-menu'].includes(page)?'':nav()}`;
 window.scrollTo(0,0);
}
function openLesson(id){const l=LESSONS.find(x=>x.id===id);if(!l)return;lessonId=id;lang=l.lang;state.last[lang]=id;save();page='lesson';render();}
function back(){if(page==='home')return false;if(page==='study'){if(study.index<study.queue.length&&!confirm('Thoát lượt học? Tiến độ các từ đã trả lời vẫn được lưu.'))return true;stopAudio();page=study.context;study=null;}else if(page==='detail')page=lastDetail;else if(page==='quiz-menu')page='lesson';else if(page==='lesson')page='library';else page='home';render();return true;}
window.handleBack=back;
function backup(){return JSON.stringify({...state,app:'Lingo',exportedAt:new Date().toISOString()},null,2);}
window.receiveBackup=raw=>{try{const proposed=validateState(JSON.parse(raw));if(!confirm('Khôi phục bản sao lưu và thay thế tiến độ hiện tại?'))return;state=proposed;save();render();toast('Đã khôi phục tiến độ.');}catch(e){toast('Bản sao lưu không hợp lệ hoặc không tương thích.');}};
document.addEventListener('click',e=>{
 const el=e.target.closest('[data-action]');if(!el||el.disabled)return;const a=el.dataset.action;
 switch(a){
 case'nav':stopAudio();page=el.dataset.page;search='';render();break;
 case'open-language':lang=el.dataset.lang;section='units';if(state.last[lang])openLesson(state.last[lang]);else{page='library';render();}break;
 case'lang':lang=el.dataset.lang;section='units';render();break;
 case'section':section=el.dataset.section;render();break;
 case'lesson':openLesson(el.dataset.id);break;
 case'back':back();break;
 case'audio':playWord(el.dataset.id);break;
 case'word':lastDetail=page;currentWord=el.dataset.id;page='detail';render();break;
 case'favorite':{const id=el.dataset.id;state.favorites=state.favorites.includes(id)?state.favorites.filter(x=>x!==id):[...state.favorites,id];save();render();break;}
 case'filter':wordFilter=el.dataset.filter;render();break;
 case'learn':{let words=lessonWords(lessonId);if(el.dataset.mode==='due')words=words.filter(w=>state.progress[w.id]?.due<=Date.now());else if(el.dataset.mode==='new'){const fresh=words.filter(w=>!state.progress[w.id]?.reps);if(fresh.length)words=fresh;}startStudy(words,'cards',LESSONS.find(x=>x.id===lessonId).short);break;}
 case'review':{const l=el.dataset.lang==='all'?null:el.dataset.lang;startStudy(dueWords(l),'cards',l?languageName(l)+' · Ôn tập':'Ôn tập hằng ngày',page);break;}
 case'review-word':startStudy([BYID[el.dataset.id]],'cards','Ôn một từ','detail');break;
 case'reveal':study.reveal=true;render();break;
 case'rate':if(!study?.reveal)break;markRated(study.queue[study.index].id,el.dataset.rating);stopAudio();study.index++;study.reveal=false;render();break;
 case'quiz-menu':page='quiz-menu';render();break;
 case'start-quiz':startStudy(lessonWords(lessonId),el.dataset.mode,LESSONS.find(x=>x.id===lessonId).short);break;
 case'answer':if(study.answered)break;answerQuestion(el.dataset.id);break;
 case'check-typing':{if(study.answered)break;const text=$('#typed-answer').value.trim();if(!text){toast('Bạn nhập câu trả lời trước nhé.');break;}const w=study.queue[study.index];answerQuestion(normalizeAnswer(text)===normalizeAnswer(w.text)?w.id:'wrong');break;}
 case'next-question':stopAudio();study.index++;study.answered=false;study.options=null;study.choice=null;render();break;
 case'exit-study':if(study.index>=study.queue.length){stopAudio();page=study.context;study=null;render();}else back();break;
 case'dark':state.settings.dark=!state.settings.dark;save();render();break;
 case'slow':state.settings.slow=!state.settings.slow;save();render();break;
 case'export':if(window.Android)Android.exportBackup(backup());else{const url=URL.createObjectURL(new Blob([backup()],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='Lingo-backup.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}break;
 case'import':if(window.Android)Android.importBackup();else $('#backup-file').click();break;
 }
});
function normalizeAnswer(s){return s.normalize('NFKC').toLowerCase().replace(/[’‘]/g,"'").replace(/[.,!?。！？]/g,'').replace(/\s+/g,' ').trim();}
function answerQuestion(id){const w=study.queue[study.index];study.choice=id;study.answered=true;if(id===w.id)study.correct++;markRated(w.id,id===w.id?'good':'again');render();}
document.addEventListener('input',e=>{if(e.target.id==='search'){const position=e.target.selectionStart;search=e.target.value;const scroll=window.scrollY;render();const field=$('#search');field.focus();field.setSelectionRange(position,position);window.scrollTo(0,scroll);}});
document.addEventListener('change',e=>{if(e.target.id==='daily-goal'){state.settings.goal=Number(e.target.value);save();toast('Đã cập nhật mục tiêu.');}if(e.target.id==='backup-file'&&e.target.files[0]){const f=e.target.files[0];if(f.size>5*1024*1024){toast('Bản sao lưu quá lớn.');return;}f.text().then(window.receiveBackup);e.target.value='';}});
document.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.id==='typed-answer'&&!study.answered){$('[data-action="check-typing"]').click();}});
window.nativeReady=()=>{readState();render();};
readState();render();
