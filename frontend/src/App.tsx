import { useState } from 'react';
import { EnvioForm } from './components/EnvioForm';
import { EnvioList } from './components/EnvioList';
import './App.css';

function App() {
    const [refreshTrigger, setRefreshTrigger] = useState(0);
    const handleSuccess = () => {
        setRefreshTrigger(prev => prev + 1);
    };

    return (
        <div className="container">
            <h1>Sistema de Gestión de Logística</h1>
            
            {/* 1. Formulario de Registro */}
            <section className="form-section">
                <EnvioForm onSuccess={handleSuccess} />
            </section>

            <hr style={{ margin: '40px 0' }} />

            {/* 2. Listado de Consultas */}
            <section className="list-section">
                <h2>Envío Registrados y Consultas</h2>
                <EnvioList refreshTrigger={refreshTrigger} />
            </section>
        </div>
    );
}

export default App;