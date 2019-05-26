import React from "react"
import withBreadcrumbs from "react-router-breadcrumbs-hoc"
import { Breadcrumb, Badge, Icon } from "antd"
import { Link } from "react-router-dom"
import { FunnelRouter } from "../../../FunnelRouter"
import "./index.less"
const RFBreadcrumbs = withBreadcrumbs(FunnelRouter)(({ breadcrumbs }) => {
  const noJumpArr = []
  return (
    <div className='RFBreadcrumbs'>
      <Breadcrumb separator={<Icon type='double-right' />}>
        {breadcrumbs.map(({ match, breadcrumb }, index) => (
          <Breadcrumb.Item key={breadcrumb.key}>
            {breadcrumbs.length - 1 === index ? (
              <Badge status='processing' text={breadcrumb} />
            ) : index <= 1 || noJumpArr.indexOf(match.url) > -1 ? null : (
              <Link
                to={{
                  pathname: match.url,
                  state: match.params ? match.params : {}
                }}
              >
                {breadcrumb}
              </Link>
            )}
          </Breadcrumb.Item>
        ))}
      </Breadcrumb>
    </div>
  )
})
export default RFBreadcrumbs
