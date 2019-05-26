import fetch from "./fetch"
const { fetchJSON } = fetch
const urls = {
  login: "/login",
  logout: "/logout"
}

export const login = (params) => {
  return fetchJSON(urls.login, { method: "post", body: params })
}

export const logout = (params) => {
  return fetchJSON(urls.logout)
}
