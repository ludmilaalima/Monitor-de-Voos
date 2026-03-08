const form = document.getElementById("monitorForm");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(e.target);
  const data = Object.fromEntries(formData.entries());

  try {
    const response = await fetch("/criar-monitor", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (!response.ok){
      console.log("Erro!", response.status, result)
      return;
      }
    
    console.log('Criado', result)
  } catch (error){
    console.log('ERRO NA REQUISICAO', error)
  }
  
})
