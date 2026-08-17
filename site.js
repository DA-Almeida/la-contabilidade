function scrollToSection(id){document.getElementById(id).scrollIntoView({behavior:'smooth'})}
function toggleMenu(){document.getElementById('navLinks').classList.toggle('mobile-open')}
function toggleFAQ(el){el.parentElement.classList.toggle('open')}
const API_URL = window.L_A_API_URL || `${window.location.origin}/api`;

async function submitContato(e){
  e.preventDefault();
  const form=e.target;
  const submit=document.getElementById('contactSubmit');
  const feedback=document.getElementById('contactFeedback');
  const data=Object.fromEntries(new FormData(form));
  submit.disabled=true;
  submit.textContent='Enviando...';
  feedback.textContent='';
  try{
    const response=await fetch(`${API_URL}/leads`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
    const result=await response.json();
    if(!response.ok)throw new Error(result.error || 'Não foi possível enviar sua mensagem.');
    feedback.style.color='var(--green)';
    feedback.textContent=`✓ ${result.message}`;
    form.reset();
  }catch(error){
    feedback.style.color='var(--red)';
    feedback.textContent=error.message || 'Não foi possível conectar ao atendimento. Tente novamente.';
  }finally{
    submit.disabled=false;
    submit.textContent='Enviar mensagem';
  }
}
