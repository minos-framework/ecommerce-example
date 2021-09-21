export const formatNumber = number => {
    return new Intl.NumberFormat('ea-ES', { style: 'currency', currency: 'EUR' }).format(number);
}

export const buildDate = date => {
    return new Date(date / 1e3);
}