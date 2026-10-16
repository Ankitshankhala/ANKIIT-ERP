import { ListRow } from '@/components/ListRow'
import { PagedList } from '@/components/PagedList'
import { formatMoney } from '@/lib/format'
import type { Product } from '@/lib/types'
import { usePagedList } from '@/lib/usePagedList'

export default function ProductsScreen() {
  const list = usePagedList<Product>('/inventory/products', 'products')

  return (
    <PagedList
      list={list}
      noun="products"
      searchPlaceholder="Search by name or SKU"
      emptyTitle="No products yet"
      emptyMessage="Products added in the web app show up here."
      renderItem={(product) => (
        <ListRow
          title={product.name}
          subtitle={[product.sku, product.category].filter(Boolean).join(' · ')}
          value={`${formatMoney(product.sale_price)} / ${product.unit_of_measure}`}
          badge={product.is_active ? null : { label: 'Inactive' }}
        />
      )}
    />
  )
}
