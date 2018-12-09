import FormData from 'form-data'

let api_root = process.env.ROOT_URL + '/api'

export function fetchWithAuth(url, options) {
    return fetch(url, {
        headers: {
            "Authorization": "Bearer " + localStorage.getItem('token'),
        },
        ...options
    })
}

/*
 * 카페 생성 API
 */
export function createCafe(data) {
    let formData = createCafeFormData(data)

    return fetchWithAuth(`${api_root}/cafes`, {method: 'POST', body: formData})
}

/*
 * 카페 리스트 API
 */
export function getCafes(sorting) {
    return fetchWithAuth(`${api_root}/cafes/?sorting=${sorting}`)
}

/*
 * 카페 상세 API
 */
export function getCafe(pk) {
    return fetchWithAuth(`${api_root}/cafes/${pk}`)
}


function createCafeFormData(data) {
    let formData = new FormData()
    let dataJson = JSON.stringify(data)

    // Cafe API는 form data로 'data' key와 'photos' key를 받을것을 기대한다
    formData.append('data', dataJson)
    if (data.photos) formData.append('photos', data.photos)

    return formData
}