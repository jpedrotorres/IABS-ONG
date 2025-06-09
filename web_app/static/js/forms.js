function clearAddressFields() {
	const logradouroField = document.querySelector('[name="logradouro"]')
	const ufField = document.querySelector('[name="uf"]')
	const nmField = document.querySelector('[name="numero_local"]')

	if (logradouroField) logradouroField.value = ''
	if (ufField) ufField.value = ''

	if (logradouroField) logradouroField.removeAttribute('readonly')
}

function fillAddressFields(data) {
	const logradouroField = document.querySelector('[name="logradouro"]')
	const ufField = document.querySelector('[name="uf"]')

	if (logradouroField && data.logradouro) logradouroField.value = data.logradouro
	if (ufField && data.uf) ufField.value = data.uf

	if (logradouroField) logradouroField.setAttribute('readonly', true)
}

function searchCep() {
	const cepField = document.querySelector('[name="cep"]')
	const ufField = document.querySelector('[name="uf"]')

	if (!cepField) {
		console.warn("Campo CEP não encontrado no DOM.")
		return
	}

	const cep = cepField.value.replace(/\D/g, '')

	if (cep.length !== 8) {
		clearAddressFields()
		return
	}
	
	clearAddressFields()
	
	fetch(`https://viacep.com.br/ws/${cep}/json/`)
	.then(response => {
		if (!response.ok) {
			throw new Error(`Erro na busca do CEP: ${response.status} ${response.statusText}`)
		}
		return response.json();
	})
	.then(data => {
		if (data.erro) {
			console.warn("CEP não encontrado pela API.")
			clearAddressFields()
		} else {
			fillAddressFields(data)
			
			if (ufField && ufField.value) {
				const userUf = ufField.value.toUpperCase()
				const apiUf = data.uf.toUpperCase()
				
				if (userUf !== apiUf) {
					console.warn(`A UF digitada (${userUf}) não corresponde à UF do CEP (${apiUf}).`)
				} 
			}
		}
	})
	.catch(error => {
		console.error("Erro ao consultar o CEP:", error)
		clearAddressFields()
	})
}

const tipoFields = document.querySelectorAll('[name="tipo"]')
let pfFieldsContainer
let pjFieldsContainer

function initPersonTypeVisibility() {
	pfFieldsContainer = document.querySelectorAll('.form-group-cpf')
	pjFieldsContainer = document.querySelectorAll('.form-group-cnpj')
	
	if (tipoFields.length === 0 || pfFieldsContainer.length === 0 || pjFieldsContainer.length === 0) {
		console.warn("Elementos PJ/PF ou CPF/CNPJ não encontrados. Verifique as classes HTML ou os nomes dos campos.")
		return
	}
	
	tipoFields.forEach(radio => {
		radio.addEventListener('change', togglePersonTypeFields)
	})
	
	togglePersonTypeFields()
}

function togglePersonTypeFields() {
	let selectedTipo = null
	tipoFields.forEach(radio => {
		if (radio.checked) {
			selectedTipo = radio.value
		}
	})
	
	pfFieldsContainer.forEach(group => group.classList.add('hidden-field'))
	pjFieldsContainer.forEach(group => group.classList.add('hidden-field'))
	
	pfFieldsContainer.forEach(group => {
		const input = group.querySelector('input')
		if (input) input.value = ''
	})
	
	pjFieldsContainer.forEach(group => {
		const input = group.querySelector('input')
		if (input) input.value = ''
	})
	
	if (selectedTipo === 'PF') {
		pfFieldsContainer.forEach(group => group.classList.remove('hidden-field'))
	} else if (selectedTipo === 'PJ') {
		pjFieldsContainer.forEach(group => group.classList.remove('hidden-field'))
	}
}

document.addEventListener("DOMContentLoaded", function() {
	const cepField = document.querySelector('[name="cep"]')
	if (cepField) {
		cepField.addEventListener('blur', searchCep)
	}
	
	initPersonTypeVisibility()
})

