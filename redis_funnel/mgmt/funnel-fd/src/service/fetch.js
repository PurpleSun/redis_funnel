import "whatwg-fetch"
import qs from "query-string"
import { notification } from "antd"
;(function() {
  try {
    new window.CustomEvent("T")
  } catch (e) {
    var CustomEvent = function(event, params) {
      params = params || { bubbles: false, cancelable: false, detail: undefined }

      var evt = document.createEvent("CustomEvent")

      evt.initCustomEvent(event, params.bubbles, params.cancelable, params.detail)

      return evt
    }
    CustomEvent.prototype = window.Event.prototype
    window.CustomEvent = CustomEvent
  }
})()

const FETCH_ERROR = "fetch_error"

function headers(options) {
  options.headers = options.headers || {}
  options.headers["X-Requested-With"] = "XMLHttpRequest"
  if (!(options.body instanceof FormData)) {
    options.headers["Content-Type"] = options.headers["Content-Type"] || "application/json"
  }
  return options
}

function credentials(options) {
  if (!options.credentials) {
    options.credentials = "same-origin"
  }
  return options
}

function cleanOptions(options) {
  //console.log('options', options)
  options = options || {}
  options.method = options.method || "GET"
  options.method = options.method.toLocaleUpperCase()
  return options
}

function params(body) {
  body = body || {}
  let query = {}
  for (let prop in body) {
    if (body.hasOwnProperty(prop)) {
      query[prop] = body[prop]
    }
  }
  return qs.stringify(query, { arrayFormat: "index" })
  //return JSON.stringify(query, {arrayFormat: 'index'});
}

function status(response) {
  //console.log("response", response)
  if (response.ok) {
    return response
  } else {
    let error = new Error(response.statusText || response.status)
    if (response.status === 504) {
      notification.error({
        message: `http请求超时，请重新加载（${response.status}）`,
        description: `${response.url}`
      })
    } else {
      notification.error({
        message: `http请求错误（${response.status}）`,
        description: `${response.url}`
      })
    }
    error.response = response
    window.dispatchEvent(
      new CustomEvent(FETCH_ERROR, {
        detail: {
          code: 1,
          status: response.status,
          msg: response.statusText
        }
      })
    )
    throw error
  }
}

export const dfetch = function(url, options) {
  options = headers(credentials(cleanOptions(options)))
  let method = options.method
  if (method === "GET") {
    if (options.type === "DELETE_GET") {
      url = url + "/" + options.body.id
    } else if (options.type === "NO_PARAM") {
      //url = url
    } else {
      if (url.indexOf("?") > -1) {
        url = [ url, params(options.body) ].join("&")
      } else {
        url = [ url, params(options.body) ].join("?")
      }
    }
    delete options.body
  } else if (method === "DELETE") {
    if (options.type !== "NO_PARAM") {
      url = url + "/" + options.body.id
    }
  } else {
    if (!(options.body instanceof FormData)) {
      options.body = JSON.stringify(options.body)
    }
  }
  //console.log('options', options, url)
  return fetch(url, options).then(status)
}

dfetch.fetchJSON = function(url, options) {
  //console.log("window.location", window.location)
  return dfetch(url, options)
    .then((res) => {
      //状态码是200，返回值为空
      return res.json().catch((res) => {
        let errmsg = "接口错误，无法将response内容转成json类型！" + res.toString()
        window.dispatchEvent(
          new CustomEvent(FETCH_ERROR, {
            detail: {
              code: 2,
              msg: errmsg
            }
          })
        )
        notification.error({
          message: "服务器错误（请联系开发者）",
          description: `${url}`
        })
        throw new Error(errmsg + url)
        //throw(errmsg + url);
        //return res
      })
    })
    .then((res) => {
      const code_first = String(res.code) ? String(res.code).substring(0, 1) : ""
      if (code_first * 1 !== 2) {
        notification.error({
          message: `${url}`,
          description: `msg:${res.msg}，code:${res.code}`
        })
      }
      if (res.code === 40005) {
        window.location.href = "/login"
      }
      return res
    })
}

export default dfetch
