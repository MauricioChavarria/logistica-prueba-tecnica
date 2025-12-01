// frontend/src/components/EnvioList.tsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/v1';
const AUTH_TOKEN = 'Bearer TEST_BEARER_TOKEN_2025';


interface Envio {
    envio_id: number;
    num_guia: string;
    tipo_logistica: 'Terrestre' | 'Maritimo';
    cliente_id: number;
    tipo_producto_id: number;
    cantidad: number;
    fecha_registro: string; 
    fecha_entrega: string; 
    precio_base: number;
    descuento_aplicado: number;
    precio_final: number; 
    placa_vehiculo: string | null;
    bodega_id: number | null;
    num_flota: string | null; 
    puerto_id: number | null;
}

interface EnvioListProps {
    refreshTrigger: number;
}

export const EnvioList: React.FC<EnvioListProps> = ({ refreshTrigger }) => {
    const [envios, setEnvios] = useState<Envio[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    

    const [filterLogistica, setFilterLogistica] = useState<'Terrestre' | 'Maritimo'>('Terrestre');
    const [filterNumGuia, setFilterNumGuia] = useState('');

  
    const fetchEnvios = async () => {
        setLoading(true);
        setError('');
        
     
        const endpoint = filterLogistica === 'Terrestre' ? 'terrestre/envios' : 'maritimo/envios';
        
        try {
            const params = filterNumGuia ? { num_guia: filterNumGuia } : {};

            const response = await axios.get<Envio[]>(`${API_BASE_URL}/${endpoint}`, {
                headers: { 'Authorization': AUTH_TOKEN },
                params: params
            });
            setEnvios(response.data);
        } catch (err: any) {
            console.error('Error fetching envios:', err);
            setError(`Error al cargar datos: ${err.response?.statusText || 'Verifique la conexión API.'}`);
            setEnvios([]);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchEnvios();
    }, [filterLogistica, refreshTrigger]);

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        fetchEnvios(); 
    };

    return (
        <div>
            {/* Controles de Filtro */}
            <form onSubmit={handleSearch} style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
                <select value={filterLogistica} onChange={(e) => setFilterLogistica(e.target.value as any)}>
                    <option value="Terrestre">Consultar Terrestres</option>
                    <option value="Maritimo">Consultar Marítimos</option>
                </select>
                <input
                    type="text"
                    placeholder="Filtrar por Número de Guía"
                    value={filterNumGuia}
                    onChange={(e) => setFilterNumGuia(e.target.value)}
                />
                <button type="submit" disabled={loading}>Buscar</button>
            </form>

            {loading && <p>Cargando envíos...</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}

            {!loading && !error && envios.length === 0 && <p>No hay envíos registrados para esta logística o el filtro no encontró resultados.</p>}

            {/* Tabla de Resultados */}
            {!loading && envios.length > 0 && (
                <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '15px' }}>
                    <thead>
                        <tr>
                            <th style={{ border: '1px solid #ccc', padding: '8px' }}>Guía</th>
                            <th style={{ border: '1px solid #ccc', padding: '8px' }}>Logística</th>
                            <th style={{ border: '1px solid #ccc', padding: '8px' }}>Cantidad</th>
                            <th style={{ border: '1px solid #ccc', padding: '8px' }}>Placa/Flota</th>
                            <th style={{ border: '1px solid #ccc', padding: '8px' }}>Precio Final</th>
                        </tr>
                    </thead>
                    <tbody>
                        {envios.map(envio => (
                            <tr key={envio.envio_id}>
                                <td style={{ border: '1px solid #ccc', padding: '8px' }}>{envio.num_guia}</td>
                                <td style={{ border: '1px solid #ccc', padding: '8px' }}>{envio.tipo_logistica}</td>
                                <td style={{ border: '1px solid #ccc', padding: '8px' }}>{envio.cantidad}</td>
                                <td style={{ border: '1px solid #ccc', padding: '8px' }}>
                                    {envio.placa_vehiculo || envio.num_flota}
                                </td>
                                <td style={{ border: '1px solid #ccc', padding: '8px' }}>
                                    ${envio.precio_final.toFixed(2)}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};