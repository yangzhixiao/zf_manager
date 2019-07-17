import * as React from 'react'
import { Table, Button } from 'antd'

const DOMAIN = 'http://zf-api.yangzhixiao.top'
// const DOMAIN = 'http://localhost:5000'

export default class ZFList extends React.Component<any, any> {

  public state = {
    data: [],
    loading: false,
  }

  public componentDidMount() {
    this.fetchData()
    // this.setState({ data: data })
  }

  public render() {
    const { data, loading } = this.state
    return (
      <Table
        style={{ padding: '15px' }}
        rowKey='id'
        loading={loading}
        dataSource={data}
        pagination={{ position: 'bottom', pageSize: 8, }}
        columns={[
          { title: '图片', dataIndex: 'imgs', 
            render: (t: any, r: any, i: number) => {
              return (
                <div>
                  <div style={{lineHeight: '20px', marginBottom: '5px', marginLeft: '10px'}}>
                    {`${r.updatetime} ${r.title}`}
                  </div>
                  {r.imgs && r.imgs.split(',').map((i: string) => 
                    <a
                      key={i}
                      href={DOMAIN + '/static/images/' + i}
                      target='_blank'
                      rel="noopener noreferrer"
                    >
                      <img
                        style={{margin: '5px'}}
                        alt={i}
                        src={DOMAIN + '/static/images/' + i.replace('.jpg', '_thumb.jpg')} 
                      />
                    </a>
                  )}
                </div>
              )
            }
          },
          { title: '操作', dataIndex: 'id', width: 150,
            render: (t: any, r: any, i: number) => {
              return (
                <Button
                  type='primary'
                  onClick={() => this.handleDownloadClick(r.id)}
                >
                  下载图片
                </Button>
              )
            }
          },
        ]}
      />
    )
  }

  public handleDownloadClick = (id: string) => {
    window.open(DOMAIN + '/download/' + id, '_blank')
  }

  public fetchData = async () => {
    this.setState({ loading: true })
    const ret = await fetch(DOMAIN + '/api/list')
    const data = await ret.json()
    this.setState({ data: data, loading: false })
  }
}