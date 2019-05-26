import fetch from "./fetch"
const { fetchJSON } = fetch
const urls = {
  login: "/login"
}

export const login = (params) => {
  return fetchJSON(urls.login, { method: "post", body: params })
}
