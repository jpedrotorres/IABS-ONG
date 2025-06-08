let genericModalDialog= null
let genericModalBackdrop= null
let genericModalPlace= null
let currentForm = null

function setupGenericModal() {
	genericModalPlace= document.querySelector("#modal-generic")
	if (!genericModalPlace) {
		console.error("Espaço para modal não encontrado (#modal-generic).");
		return;
	}
}

function openGenericModal(genericModalUrl, modalData, onConfirmActionCallback = null) {
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
		
		const confirmButton = genericModalPlace.querySelector('.btn-confirm-primary')
		if (confirmButton) {
			confirmButton.addEventListener('click', function(event) {
				event.preventDefault()
				
				if (onConfirmActionCallback && typeof onConfirmActionCallback === 'function') {
					onConfirmActionCallback()
				}
				closeGenericModal()
			})
		}

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

function confirmGenericModal() {
	closeGenericModal()
	form.submit()
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

const confirmFormButton = document.querySelector("#btn-confirm-action-data")
if (confirmFormButton) {
	confirmFormButton.addEventListener("click", function(event) {
		event.preventDefault()
		console.log("Botão de confirmar formulário CLICADO. event.preventDefault() chamado.")

		
		currentForm = confirmFormButton.closest("form")
		if (!currentForm) {
			console.error("Não foi possível encontrar o formulário pai do botão de confirmação.")
		return
		}
		console.log("Formulário pai encontrado:", currentForm)
		
		const entityType = confirmFormButton.dataset.entityType
		const actionType = confirmFormButton.dataset.actionType
		const objectId = confirmFormButton.dataset.objectId
		
		const modalUrl = confirmFormButton.dataset.modalUrl

		if (!entityType || !actionType || !modalUrl) {
			console.error("Dados insuficientes para abrir o modal.")
			return
		}		

		openGenericModal(modalUrl, {
			type: actionType,
			entity_type: entityType,
			object_id: objectId
		}, () => {
			console.log("Modal confirmado. Tentando submeter formulário AJAX...")
			let finalRedirectUrl = null
			if (genericModalPlace) {
				const tempElement = genericModalPlace.querySelector('.btn-confirm-primary')
				if (tempElement) {
					finalRedirectUrl = tempElement.getAttribute('href')
					console.log("URL de redirecionamento final capturada da modal:", finalRedirectUrl)
				} else {
					console.warn("Elemento .btn-confirm-primary não encontrado em genericModalPlace ao capturar finalRedirectUrl.")
				}
			} else {
				console.warn("genericModalPlace é null ao tentar capturar finalRedirectUrl.")
			}

			if (currentForm) {
				const formData = new FormData(currentForm)
				const formActionUrl = currentForm.getAttribute('action')
				console.log("Submetendo formulário para URL:", formActionUrl)
				
				fetch(formActionUrl, {
					method: 'POST',
					headers: {
						'X-CSRFToken': getCookie('csrftoken'),
						'X-Requested-With': 'XMLHttpRequest'
					},
					body: formData
				})
				.then(response => {
					console.log("Resposta do servidor recebida. Status:", response.status)

					if (!response.ok) {
						return response.json().then(err => {
							throw new Error(err.error || `Erro na submissão do formulário: ${response.status} ${response.statusText}`)
						}).catch(() => {
							throw new Error(`Erro na submissão do formulário: ${response.status} ${response.statusText}`)
						})
					}
					return response.json();
				})
				.then(formResponseData => {
					console.log("Formulário submetido com sucesso!", formResponseData);
					
					closeGenericModal()
					
					if (actionType === 'cadastro' && formResponseData.detail_url) {
						window.location.href = formResponseData.detail_url
					} else if (finalRedirectUrl) {
						window.location.href = finalRedirectUrl
					} else {
						console.warn("Nenhuma URL final de redirecionamento definida.")
						window.location.reload()
					}
				})
				.catch(error => {
					console.error("Erro ao submeter o formulário via AJAX:", error)
					clearFormErrors(currentForm)
					
					if (error.formErrors) {
						displayFormErrors(currentForm, error.formErrors)
						alert("Por favor, corrija os erros no formulário.")
					} else {
						alert(error.message || "Ocorreu um erro inesperado ao salvar o formulário. Tente novamente.")
					}
					
				})
			} else {
				console.warn("Nenhum formulário encontrado para submeter.")
			}
		})
	})
}

function clearFormErrors(form) {
	const nonFieldErrorsList = form.querySelector('.nonfield-errors')
	if (nonFieldErrorsList) {
		nonFieldErrorsList.innerHTML = ''
	}
	
	form.querySelectorAll('.errorlist').forEach(errorList => {
		errorList.innerHTML = ''
	})
	
	form.querySelectorAll('.form-group .form-control').forEach(field => {
		field.classList.remove('is-invalid')
	})
}

function displayFormErrors(form, errors) {
	if (errors.__all__) {
		let nonFieldErrorsList = form.querySelector('.nonfield-errors')
		if (!nonFieldErrorsList) {
			nonFieldErrorsList = document.createElement('ul')
			nonFieldErrorsList.className = 'errorlist nonfield-errors'
			form.prepend(nonFieldErrorsList)
		}
		
		nonFieldErrorsList.innerHTML = ''
		errors.__all__.forEach(error => {
			const li = document.createElement('li')
			li.textContent = error
			nonFieldErrorsList.appendChild(li)
		})
	}
	
	for (const fieldName in errors) {
		if (fieldName === '__all__') continue
		
		const field = form.querySelector(`[name="${fieldName}"]`)
		if (field) {
			field.classList.add('is-invalid')
			
			let errorList = field.closest('.form-group') ? field.closest('.form-group').querySelector('.errorlist') : null
			if (!errorList) {
				errorList = document.createElement('ul')
				errorList.className = 'errorlist'
				field.parentNode.insertBefore(errorList, field.nextSibling)
			}
			errorList.innerHTML = ''
			errors[fieldName].forEach(error => {
				const li = document.createElement('li')
				li.textContent = error
				errorList.appendChild(li)
			})

		}
	}
}

const relatorioButtons= document.querySelectorAll(".btn-show-relatorio")
if (relatorioButtons.length>0) {
	relatorioButtons.forEach(button => {
		button.addEventListener("click", function(event) {
			event.preventDefault()

			const checkUrl = button.dataset.checkUrl
			const modalUrl = button.dataset.modalUrl

			fetch(checkUrl)
			.then(response => response.json())
			.then(data => {
				if(!data.tem_relatorio) {
					openGenericModal(modalUrl, { type: 'aviso_relatorio' })
				} else {
					window.open(data.relatorio_url, "_blank")
				}
			})
			.catch(error => {
				console.error("Erro ao verificar o relatório:", error)
			})
		})
	})
}

document.addEventListener("DOMContentLoaded", setupGenericModal)
