import React, { useState } from 'react';
import Button from '../UI/Button';
import Textarea from '../UI/Textarea';

const ChatInput = ({ onSend, onStop, disabled, isGenerating }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSend(input.trim());
      setInput('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-3 w-full">
      <Textarea
        placeholder="请输入考研英语相关问题..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        className="flex-1 min-h-[120px] max-h-[300px] text-lg"
      />
      {isGenerating ? (
        <Button
          type="button"
          onClick={onStop}
          className="self-end px-6 py-3 text-base"
        >
          停止
        </Button>
      ) : (
        <Button
          type="submit"
          disabled={!input.trim() || disabled}
          className={`self-end px-6 py-3 text-base ${
            !input.trim() && !disabled ? 'opacity-60 cursor-not-allowed' : ''
          }`}
        >
          {disabled ? '⏳' : '发送'}
        </Button>
      )}
    </form>
  );
};

export default ChatInput;
