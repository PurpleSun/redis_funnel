import React, { Component } from "react"
import { withRouter } from "react-router-dom"
import { Form, Icon, Input, Button, message } from "antd"
import { login } from "../../service/login"
import "./index.less"
class LoginPage extends Component {
  constructor(props) {
    super(props)
    this.state = {
      loginLoading: false
    }
  }
  handleSubmit = (e) => {
    e.preventDefault()
    this.props.form.validateFields((err, values) => {
      if (!err) {
        console.log("Received values of form: ", values)
        let formData = new FormData()
        formData.append("username", values.username)
        formData.append("password", values.password)
        this.setState({
          loginLoading: true
        })
        login(formData).then((res) => {
          console.log(res)
          this.setState({
            loginLoading: false
          })
          if (res.code === 20000) {
            message.success("登录成功！")
          } else {
            message.error("登录失败！")
          }
          //   if(res.code)
        })
      }
    })
  }
  render() {
    let { loginLoading } = this.state
    const { getFieldDecorator } = this.props.form

    return (
      <div className='Login'>
        <div className='loginContent'>
          <div className='loginHeader'>
            <img className src={require("../../assets/img/logo.svg")} />
            Redis-Funnel
          </div>
          <div className='loginSubHeader'>A distributed funnel middleware based on redis</div>
          <div className='loginForm'>
            <Form onSubmit={this.handleSubmit} className='login-form'>
              <Form.Item>
                {getFieldDecorator("username", {
                  rules: [ { required: true, message: "Please input your username!" } ]
                })(<Input prefix={<Icon type='user' style={{ color: "rgba(0,0,0,.25)" }} />} placeholder='Username' />)}
              </Form.Item>
              <Form.Item>
                {getFieldDecorator("password", {
                  rules: [ { required: true, message: "Please input your Password!" } ]
                })(<Input prefix={<Icon type='lock' style={{ color: "rgba(0,0,0,.25)" }} />} type='password' placeholder='Password' />)}
              </Form.Item>
              <Form.Item>
                <Button loading={loginLoading} type='primary' htmlType='submit' className='login-form-button'>
                  Log in
                </Button>
              </Form.Item>
            </Form>
          </div>
        </div>
      </div>
    )
  }
}

const Login = Form.create({ name: "login" })(LoginPage)
export default withRouter(Login)
