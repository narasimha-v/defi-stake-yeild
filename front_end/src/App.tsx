import { Container } from '@material-ui/core';
import { DAppProvider, Kovan } from '@usedapp/core';
import React from 'react';
import { Header, Main } from './components';

function App() {
	return (
		<DAppProvider
			config={{
				networks: [Kovan],
				notifications: {
					expirationPeriod: 1000,
					checkInterval: 1000
				}
			}}>
			<Header />
			<Container maxWidth='md'>
				<Main />
			</Container>
		</DAppProvider>
	);
}

export default App;
