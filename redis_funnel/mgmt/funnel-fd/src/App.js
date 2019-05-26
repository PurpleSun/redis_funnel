import React from "react"
import { Layout, Menu, Icon } from "antd"
import { Route, Switch, withRouter } from "react-router-dom"
import Login from "./pages/Login"
import "./App.less"

const { Header, Content, Footer, Sider } = Layout
class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {}
  }
  componentWillReceiveProps(nextPorps) {}
  render() {
    let isLogin = false
    console.log(this.props)
    if (this.props.location.pathname.indexOf("/login") > -1) {
      isLogin = true
    }
    return (
      <div className='App'>
        {isLogin ? (
          <Login />
        ) : (
          <Layout>
            <Sider
              width={250}
              style={{
                overflow: "auto",
                height: "100vh",
                position: "fixed",
                left: 0
              }}
            >
              <div className='logo'>
                <img className='logoImg' src={require("./assets/img/logo.svg")} />
                <h1 className='logoText'>Redis-Funnel</h1>
              </div>
              <Menu theme='dark' mode='inline' defaultSelectedKeys={[ "1" ]}>
                <Menu.Item key='1'>
                  <Icon type='unordered-list' />
                  <span className='nav-text'>列表</span>
                </Menu.Item>
              </Menu>
            </Sider>
            <Layout style={{ marginLeft: 250 }}>
              <Header style={{ background: "#fff", padding: 0 }} />
              <Content style={{ margin: "24px 16px 0", overflow: "initial" }}>
                <div style={{ padding: 24, background: "#fff", textAlign: "center" }}>
                  <Switch>
                    <Route path='/login' component={Login} exact />
                  </Switch>
                </div>
              </Content>
              <Footer style={{ textAlign: "center" }}>Redis-Funnel-FD ©2019 Created by Jserk</Footer>
            </Layout>
          </Layout>
        )}
      </div>
    )
  }
}

export default withRouter(App)
