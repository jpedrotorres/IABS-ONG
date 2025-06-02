let genericModalDialog= null
let genericModalBackdrop= null
let genericModalPlace= null

function setupGenericModal() {
	genericModalPlace= document.querySelector("#modal-generic")
	if (!genericModalPlace) {
		console.error("Espaço para modal não encontrado (#modal-generic).");
		return;
	}
}

function openGenericModal(genericModalUrl, modalData) {
	if (!modalData || typeof modalData != 'object') {
		console.error("Dados do modal inválidos. Esperava um objeto.");
		return;
	}
	
	fetch(genericModalUrl, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': getCookie('csrftoken')
		},
		body: JSON.stringify(modalData)
	})
	.then(response => {
		if (!response.ok) {
			return response.json().then(err => {
				throw new Error(err.error || `Erro HTTP: ${response.status} ${response.statusText}`)
			}).catch(() => {
				throw new Error(`Erro HTTP: ${response.status} ${response.statusText}`)
			})
		}
		return response.text()
	})
	.then(html => {
		genericModalPlace.innerHTML= html
		genericModalDialog= document.querySelector("#modal-dialog")
		genericModalBackdrop= document.querySelector("#modal-backdrop")
		
		if (!genericModalDialog || !genericModalBackdrop) {
			console.error("Elementos do modal (dialog ou backdrop) não encontrados após a inserção do HTML.")
			return
		}

		const closeButtons = genericModalDialog.querySelectorAll('.btn-cancel')
		closeButtons.forEach(button => {
			button.addEventListener('click', closeGenericModal);
		})
		
		genericModalBackdrop.addEventListener("click", function(event) {
			if (event.target == genericModalBackdrop) closeGenericModal()
		})

		showGenericModal()
	})
	.catch(error => console.error("Erro ao carregar o modal de saída:", error))
}

function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie != '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			if (cookie.startsWith(name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

function showGenericModal() {
	if (genericModalDialog && genericModalBackdrop) {
		genericModalDialog.style.display= "block"
		genericModalBackdrop.style.display= "block"

		document.body.classList.add("modal-open")
	}
}

function closeGenericModal() {
	if (genericModalDialog && genericModalBackdrop) {
		genericModalDialog.style.display= "none"
		genericModalBackdrop.style.display= "none"

		document.body.classList.remove("modal-open")
		genericModalPlace.innerHTML= ""
		genericModalDialog = null
		genericModalBackdrop = null
	}
}

const logoutButton= document.querySelector("#btn-logout")
if (logoutButton) {
	logoutButton.addEventListener("click", function(event) {
		event.preventDefault()
		const logoutUrl= logoutButton.dataset.modalUrl
		console.log("URL de modal de logout sendo usada:", logoutUrl)
		openGenericModal(logoutUrl, {type: 'logout' })
	})
}

document.addEventListener("DOMContentLoaded", setupGenericModal)
