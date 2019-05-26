import React from "react"
import { Layout, Menu, Icon, Dropdown } from "antd"
import { Route, Switch, withRouter } from "react-router-dom"
import Login from "./pages/Login"
import LeftMenu from "./pages/Components/LeftMenu"
import BreadCrumbs from "./pages/Components/BreadCrumbs"
import { FunnelRouter } from "./FunnelRouter"
import { logout } from "./service/login"
import "./App.less"

const { Header, Content, Footer, Sider } = Layout
class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {}
  }
  componentWillReceiveProps(nextPorps) {}
  fetchLogout = () => {
    logout().then((res) => {
      if (res.code === 20000) {
        this.props.history.push("/login")
      }
    })
  }
  render() {
    let isLogin = false
    if (this.props.location.pathname.indexOf("/login") > -1) {
      isLogin = true
    }
    const menu = (
      <Menu>
        <Menu.Item onClick={this.fetchLogout}>注销</Menu.Item>
      </Menu>
    )
    return (
      <div className='App'>
        {isLogin ? (
          <Login />
        ) : (
          <Layout style={{ height: "100%" }}>
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
              <LeftMenu />
            </Sider>
            <Layout style={{ marginLeft: 250, height: "100%" }}>
              <Header style={{ background: "#fff", padding: 0 }}>
                <div className='userInfoBox'>
                  <Dropdown overlay={menu} placement='bottomLeft'>
                    <span>
                      <img className='userLogo' src={require("./assets/img/user_logo.svg")} alt='' />Admin
                    </span>
                  </Dropdown>
                </div>
              </Header>
              <Content style={{ margin: "24px 16px 0", overflow: "initial" }}>
                <div style={{ padding: 24, background: "#fff", textAlign: "center", minHeight: "100%" }}>
                  <BreadCrumbs />
                  <Switch>
                    {FunnelRouter.map((item) => {
                      return <Route path={item.path} component={item.component} exact />
                    })}
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
