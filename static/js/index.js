function showNotification(message,  type = 'success') {
    const notification = document.createElement('div');
    notification.classList.add('notification', type);
    notification.textContent = message;

    document.getElementById('notifications').appendChild(notification);

    // hide notification after 6 seconds
    setTimeout(() => {
        notification.classList.add('hide');
        setTimeout(() => notification.remove(), 500); // حذف از DOM پس از محو شدن
    }, 7000);
}