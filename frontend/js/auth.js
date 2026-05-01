(function(){
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');
  const currentPage = window.location.pathname.split('/').pop();

  // Redirect driver away from user/admin pages
  const driverOnlyPage = 'driver-dashboard.html';
  const userPages = ['dashboard.html','prediction.html','realtime.html','zones.html',
                     'heatmap.html','driver.html','peak.html','insights.html',
                     'visualization.html','admin.html'];
  if (role === 'driver' && userPages.includes(currentPage)) {
    window.location.href = 'driver-dashboard.html';
    return;
  }

  if(token){
    document.getElementById('nav-login').style.display='none';
    document.getElementById('nav-logout').style.display='inline-block';
  }

  const adminBtn = document.getElementById('nav-admin');
  if(adminBtn && role !== 'admin'){
    adminBtn.style.display='none';
  }

  if(role === 'admin'){
    document.querySelectorAll('.user-only').forEach(el => el.style.display='none');
    document.querySelectorAll('.admin-only').forEach(el => el.style.display='');
  } else {
    document.querySelectorAll('.admin-only').forEach(el => el.style.display='none');
  }

  document.getElementById('nav-logout').addEventListener('click',function(e){
    e.preventDefault();
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('name');
    localStorage.removeItem('user_id');
    window.location.href='/pages/login.html';
  });
})();
