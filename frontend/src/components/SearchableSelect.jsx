import Select from 'react-select'

const SearchableSelect = ({ value, onChange, options, placeholder = "Search...", label, ...props }) => {
  const selectOptions = Array.isArray(options) && typeof options[0] === 'string'
    ? options.map(opt => ({ value: opt, label: opt }))
    : options

  const customStyles = {
    control: (base) => ({
      ...base,
      minHeight: '42px',
      borderColor: '#e1e8ed',
      '&:hover': {
        borderColor: '#0066cc'
      }
    }),
    menu: (base) => ({
      ...base,
      zIndex: 100
    })
  }

  return (
    <div className="form-group">
      {label && <label className="form-label">{label}</label>}
      <Select
        value={value}
        onChange={onChange}
        options={selectOptions}
        placeholder={placeholder}
        isClearable
        isSearchable
        styles={customStyles}
        {...props}
      />
    </div>
  )
}

export default SearchableSelect
