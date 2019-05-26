import React, { Component } from "react"
import { Table, Button } from "antd"
import { funnelInfo } from "../../service/funnel"

class Funnel extends Component {
  constructor(props) {
    super(props)
    this.state = {
      funnelInfo: {}
    }
  }
  componentDidMount() {
    this.fetchFunnelInfo()
  }

  fetchFunnelInfo = () => {
    let { funnelName } = this.props.match.params
    funnelInfo(funnelName).then((res) => {
      if (res.code === 20000) {
        this.setState({
          funnelInfo: res.data.funnel
        })
      }
    })
  }
  render() {
    const { funnelInfo } = this.state
    let columns = [
      {
        title: "key",
        key: "key",
        dataIndex: "key"
      },
      {
        title: "value",
        key: "value",
        dataIndex: "value"
      }
    ]
    let funnelInfoKeyValueList = []
    Object.keys(funnelInfo).map((item) => {
      funnelInfoKeyValueList.push({
        key: item,
        value: funnelInfo[item]
      })
    })
    return (
      <div className='Funnel'>
        <Table rowKey='name' dataSource={funnelInfoKeyValueList} columns={columns} pagination={false} />
      </div>
    )
  }
}
export default Funnel
