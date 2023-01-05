import { PUBLIC_BACKEND_URL } from '$env/static/public'
import { PUBLIC_USE_TLS } from '$env/static/public'

export const HTTP_PROTOCOL = PUBLIC_USE_TLS === 'false' ? 'http' : 'https'

const backendUrl = PUBLIC_BACKEND_URL || 'localhost:8000'

export const API_URL = `${HTTP_PROTOCOL}://${backendUrl}`
export default {url: API_URL, httpProtocol: HTTP_PROTOCOL}
