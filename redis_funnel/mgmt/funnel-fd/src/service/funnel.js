import fetch from "./fetch"
const { fetchJSON } = fetch
const urls = {
  group: "/api/group",
  funnel: "/api/key"
}

export const groupList = (params) => {
  return fetchJSON(urls.group)
}

export const funnelList = (key) => {
  return fetchJSON(`${urls.group}/${key}`)
}

export const funnelInfo = (key) => {
  return fetchJSON(`${urls.funnel}/${key}`)
}

export const deletefunnel = (key) => {
  return fetchJSON(`${urls.funnel}/${key}`, {
    method: "DELETE"
  })
}
