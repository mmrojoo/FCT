document.addEventListener('DOMContentLoaded', () => {
  const registerForm = document.getElementById('register-form');

  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const nombre = document.getElementById('nombre').value;
    const apellidos = document.getElementById('apellidos').value;
    const correoElectronico = document.getElementById('correoElectronico').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
      const response = await fetch('/api/users/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nombre, apellidos, correoElectronico, username, password })
      });

      const data = await response.json();

      if (response.ok) {
        alert('Usuario registrado con éxito');
        // Aquí puedes redirigir al usuario a otra página o realizar otras acciones
      } else {
        alert(data.message || 'Error al registrar usuario');
      }
    } catch (error) {
      console.error('Error al registrar usuario', error);
      alert('Error al registrar usuario');
    }
  });
});
