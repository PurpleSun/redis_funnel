import React, { Component } from "react"
import { withRouter } from "react-router-dom"
import { Menu, Icon } from "antd"
import { groupList } from "../../../service/funnel"
import "./index.less"

const { SubMenu } = Menu
class LeftMenu extends Component {
  constructor(props) {
    super(props)
    this.state = {
      groupList: [],
      selectedKeys: [ "" ]
    }
  }
  componentDidMount() {
    this.fetchGroupList()
  }
  componentWillReceiveProps(nextProps) {
    let groupId = nextProps.location.pathname.split("/")[2]
    this.setState({
      selectedKeys: [ groupId ]
    })
  }
  getActiveKeys = () => {}
  fetchGroupList = () => {
    groupList().then((res) => {
      if (res.code === 20000) {
        let groupList = res.data.group_list
        let groupId = this.props.location.pathname.split("/")[2]
        this.setState({
          groupList
        })
        if (groupList.length > 0 && !groupId) {
          this.props.history.push(`/group/${groupList[0]}`)
        }
      }
    })
  }
  render() {
    const { groupList, selectedKeys } = this.state
    console.log(selectedKeys)
    return (
      <div className='LeftMenu'>
        <Menu theme='dark' mode='inline' defaultOpenKeys={[ "group" ]} selectedKeys={selectedKeys}>
          <SubMenu
            key='group'
            title={
              <span>
                <Icon type='unordered-list' />
                <span>分组</span>
              </span>
            }
          >
            {groupList.map((item, index) => {
              return (
                <Menu.Item
                  onClick={() => {
                    this.props.history.push(`/group/${item}`)
                  }}
                  key={item}
                >
                  <Icon type='table' />
                  <span className='nav-text'>{item}</span>
                </Menu.Item>
              )
            })}
          </SubMenu>
        </Menu>
      </div>
    )
  }
}

export default withRouter(LeftMenu)
