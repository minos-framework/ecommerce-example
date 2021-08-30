export const formatNumber = number => {
    return new Intl.NumberFormat('ea-ES', { style: 'currency', currency: 'EUR' }).format(number);
}