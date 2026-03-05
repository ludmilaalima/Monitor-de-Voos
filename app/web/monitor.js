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


  if (!response.ok){
    //const msg = await response.json();
    console.log(response.status)

    }

  const result = await response.json();
  console.log('Criado', result)
  





/*
 10) Se o backend responder erro (status 400/500 etc), cai aqui
    if (!response.ok) {
      // Tenta ler uma mensagem do backend (se ele enviar)
      const errText = await response.text();
      throw new Error(errText || `Erro HTTP: ${response.status}`);
    }

    // 11) Tenta ler a resposta como JSON (bem comum em APIs)
    const result = await response.json();

    // 12) Mostra no console (pra debug)
    console.log("Monitor criado:", result);

    // 13) Você pode avisar na tela também
    alert("Monitoração iniciada com sucesso!");
    
    // (Opcional) Limpar formulário após sucesso
    form.reset();

  } catch (err) {
    // 14) Qualquer erro de rede/parse/status cai aqui
    console.error("Erro ao criar monitor:", err);
    alert("Não foi possível iniciar a monitoração. Veja o console para detalhes.");
  }
})*/