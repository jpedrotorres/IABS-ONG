let modalSystemOut= null
let modalBackdrop= null
let modalPlace= null

function openModal() {
	const logoutButton= document.querySelector("#btn-logout")
	modalPlace= document.querySelector("#modal-logout")

	if(logoutButton) {
		const modalUrl = logoutButton.dataset.modalUrl

		logoutButton.addEventListener("click", function(event) {
			event.preventDefault()

			if (!modalUrl) {
				console.error("URL do modal de logout não encontrada no data-modal-url do botão.")
				return
			}

			fetch(modalUrl)
			.then(response => response.text())
			.then(html => {
				modalPlace.innerHTML= html
				modalSystemOut= document.querySelector("#modal-dialog")
				modalBackdrop= document.querySelector("#modal-backdrop")

				const btnCancel= document.querySelector(".btn-cancel")
				btnCancel.addEventListener("click", closeModal)

				showModal()
			})
			.catch(error => console.error("Erro ao carregar o modal de saída:", error))
		})
	}

	if (modalPlace) {
		modalPlace.addEventListener("click", function(event) {
			if (event.target== modalBackdrop) closeModal()
		})
	}
}

function showModal() {
	if (modalSystemOut && modalBackdrop) {
		modalSystemOut.style.display= "block"
		modalBackdrop.style.display= "block"

		document.body.classList.add("modal-open")
	}
}

function closeModal() {
	if (modalSystemOut && modalBackdrop) {
		modalSystemOut.style.display= "none"
		modalBackdrop.style.display= "none"

		document.body.classList.remove("modal-open")
		modalPlace.innerHTML= ""
	}
}

document.addEventListener("DOMContentLoaded", openModal)
