import Group from "./pages/Group"
import Funnel from "./pages/Funnel"
export const FunnelRouter = [
  {
    path: "/group/:groupId",
    breadcrumb: "漏斗列表",
    component: Group
  },
  {
    path: "/group/:groupId/:funnelName",
    breadcrumb: "漏斗详情",
    component: Funnel
  }
]
