import React from 'react';
import {View, Text} from 'react-native';
import colors from './src/config/colors';
import strings from './src/config/strings';

const App = () => {
  return (
    <View
      style={{
        backgroundColor: colors.primary,
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
      }}>
      <Text style={{color: colors.secondary}}>
        This is {strings.welcomeMessage}
      </Text>
    </View>
  );
};

export default App;
