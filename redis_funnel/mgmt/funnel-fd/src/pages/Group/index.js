import React, { Component } from "react"
import { withRouter } from "react-router-dom"
import { Table, Button } from "antd"
import { funnelList } from "../../service/funnel"
import "./index.less"
class Group extends Component {
  constructor(props) {
    super(props)
    this.state = {
      funnelList: []
    }
  }
  componentDidMount() {
    this.fetchFunnelList()
  }
  fetchFunnelList = () => {
    console.log(this.props)
    let { groupId } = this.props.match.params
    funnelList(groupId).then((res) => {
      if (res.code === 20000) {
        this.setState({
          funnelList: res.data.funnel_list
        })
      }
    })
  }
  render() {
    let { groupId } = this.props.match.params
    const { funnelList } = this.state
    const columns = [
      {
        title: "名称",
        key: "name",
        dataIndex: "name",
        render: (text, record) => {
          return (
            <a
              onClick={() => {
                this.props.history.push(`/group/${groupId}/${text}`)
              }}
            >
              text
            </a>
          )
        }
      },
      {
        title: "leaking_ts",
        key: "leaking_ts",
        dataIndex: "leaking_ts"
      },
      {
        title: "left_quota",
        key: "left_quota",
        dataIndex: "left_quota"
      },
      {
        title: "capacity",
        key: "capacity",
        dataIndex: "capacity"
      },
      {
        title: "operations",
        key: "operations",
        dataIndex: "operations"
      },
      {
        title: "seconds",
        key: "seconds",
        dataIndex: "seconds"
      },
      {
        title: "操作",
        key: "operation",
        dataIndex: "seconds",
        render: (text, record) => {
          return <a>删除</a>
        }
      }
    ]
    return (
      <div className='Group'>
        <Button className='createFunnelBtn' type='primary'>
          新建漏斗
        </Button>
        <Table rowKey='name' dataSource={funnelList} columns={columns} pagination={false} />
      </div>
    )
  }
}

export default withRouter(Group)
