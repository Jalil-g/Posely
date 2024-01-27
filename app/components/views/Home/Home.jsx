import { Text, View } from 'react-native';
import { Button } from 'react-native-paper';

export default function Home({ navigation }) {

    return (
        <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
            <Button icon="camera" mode="contained" onPress={() => navigation.navigate('Camera')}>Click picture</Button>
        </View>
    );
}